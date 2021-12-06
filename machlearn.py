import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

import numpy as np
from datetime import datetime,timedelta
from statsmodels.tsa.stattools import adfuller
import statsmodels.tsa.stattools as ts
import statsmodels.formula.api as sm
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

######### Define utility functions###########################
@st.cache
def get_stock(ticker,start_date,end_date):
    sym = yf.download(ticker,start_date=start_date,end_date=end_date)
    sym = sym.drop(['Volume'],axis=1)
    stock = sym.mean(axis=1)
    return stock

@st.cache
def get_ratio(sym1,sym2):
    ratio_price = sym1/sym2
    #ratio_price = ratio_price.dropna()
    idx = sym1.index
    ratio = pd.DataFrame(data=ratio_price,index=idx)    
    ratio = ratio.rename(columns={0:'ratio price'})
    ratio = ratio.dropna()
    ratio.index = ratio.index.strftime("%Y%m%d")
    #ratio = ratio.set_index('Date')
    ratio.reset_index(inplace=True)
    

    #ratio = pd.DataFrame(index=ratio_price.index)
    #ratio['ratio_price'] = ratio_price
    #ratio.rename(columns={ratio.index:'Date'})
    return ratio


def plot_ratio(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index,y=data['ratio price']))
    fig.layout.update(title_text='Time Series Data',xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


#####################################################################


def app():
    st.title("Machine Learning for Stocks Prediction")
    st.markdown("Time Series in Finance are always not stationary, that's why we're going to analyze pairs of stocks")
    ticker_1 = st.text_input('Insert the symbol of the first ticker','')
    ticker_2 = st.text_input('Insert the symbol of the second ticker','')

        #insert date
    today = datetime.today()
    days = timedelta(1)
    yesterday = today - days
    start_date = st.date_input(label='Insert start date',value=yesterday,max_value=yesterday)
    end_date = st.date_input(label='Insert end date',max_value=today)


    if st.button('Submit'):
        try:
            stock1 = get_stock(ticker_1,start_date,end_date)
            stock2 = get_stock(ticker_2,start_date,end_date)
        except ValueError:
            st.error("Control the correct format of ticker and date")

        n_years = 1 #st.slider("Years of prediction:",1,3)
        period = n_years * 5
        ratio = get_ratio(stock1,stock2)
        st.dataframe(ratio)
        

        if adfuller(ratio['ratio price'])[1] < 0.5:
            
            

            plot_ratio(ratio)

            #forecast
            
            df_train = ratio[['Date','ratio price']]
            df_train = df_train.rename(columns={"Date":"ds","ratio price":"y"})

            with st.spinner("Waiting for the prediction"):
                m = Prophet()
                m.fit(df_train)
                future = m.make_future_dataframe(periods=period)
                forecast = m.predict(future)

                st.subheader('Forecast Data')
                st.write(forecast.tail())
                f_forecast=(pd.DataFrame(forecast))
                st.download_button(label="Download CSV",data=f_forecast.to_csv(),mime='text/csv')
                
                st.write('Forecast data')
                fig1 = plot_plotly(m,forecast)
                st.plotly_chart(fig1)

                st.write('forecast components')
                fig2 = m.plot_components(forecast)
                st.write(fig2)
            st.success("Done!")

        else:
            st.warning("Ernest P. Chan's words echoed...There is a time and place for everything but data needs to be stationary.")
    else:
        st.error('Insert the right symbol name')    

if __name__== "__main__":
    app()



#streamlit run test.py

