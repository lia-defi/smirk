import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import sklearn as skl
import numpy as np
from datetime import date, datetime,timedelta
from statsmodels.tsa.stattools import adfuller
import statsmodels.tsa.stattools as ts
import statsmodels.formula.api as sm



def app():

    st.title('Statistical Arbitrage')
    st.text("Statistical arbitrage, also referred to as stat arb,")
    st.text("is a computationally intensive approach to algorithmically trading financial market assets such as equities and commodities.")
    st.text("It involves the simultaneous buying and selling of security portfolios according to predefined or adaptive statistical models.")
    st.text("Statistical arbitrage techniques are modern variations of the classic cointegration-based pairs trading strategy.")
    st.text("This strategy is based on short-term mean reversion principles coupled with hedging strategies that take care of overall market risk.")
           

    ticker_1 = st.text_input('Insert the symbol of the first ticker','')
    ticker_2 = st.text_input('Insert the symbol of the second ticker','')

    #insert date
    today = datetime.today()
    days = timedelta(1)
    yesterday = today - days
    start_date = st.date_input(label='Insert start date',value=yesterday,max_value=yesterday)
    end_date = st.date_input(label='Insert end date',max_value=today)



    try:
        if st.button('Submit'):

            ticker_data_1 = yf.download(ticker_1,start=start_date,end=end_date)
            ticker_data_2 = yf.download(ticker_2,start=start_date,end=end_date)
            price_1 = ticker_data_1.drop(['Volume'],axis=1)

            price_2 = ticker_data_2.drop(['Volume'],axis=1)
            price_1 = price_1.mean(axis=1)
            price_2 = price_2.mean(axis=1)

            ratio = price_1/price_2
            #spread = price_1-price_2

            ratio = ratio.dropna()
            #spread = spread.dropna()

            if adfuller(ratio)[1] < 0.5:
                with st.spinner("Waiting for the prediction"):
                    #plot Ratio
                    st.info('Ratio')

                    fig = plt.figure(figsize=(12,6))
                    plt.plot(ratio)
                    plt.xlabel('Period')
                    st.pyplot(fig)

                    df = pd.DataFrame(index=price_1.index)
                    df['sym1'] = price_1
                    df['sym2'] = price_2
                    df = df.dropna()
                    coint_res = ts.coint(df['sym1'],df['sym2'])
                    lookback = 20
                    hedgeRatio=np.full(df.shape[0], np.nan)
                    for t in np.arange(lookback, len(hedgeRatio)):
                        regress_results=sm.ols(formula="sym1 ~ sym2", data=df[(t-lookback):t]).fit() # Note this can deal with NaN in top row
                        hedgeRatio[t-1]=regress_results.params[1]
                    yport=np.sum(ts.add_constant(-hedgeRatio)[:, [1,0]]*df, axis=1)


                    # Bollinger band strategy
                    entryZscore=1
                    exitZscore=0

                    MA=yport.rolling(lookback).mean()
                    MSTD=yport.rolling(lookback).std()
                    zScore=(yport-MA)/MSTD

                    longsEntry=zScore < -entryZscore
                    longsExit =zScore > -entryZscore

                    shortsEntry=zScore > entryZscore
                    shortsExit =zScore < exitZscore

                    numUnitsLong=np.zeros(longsEntry.shape)
                    numUnitsLong[:]=np.nan

                    numUnitsShort=np.zeros(shortsEntry.shape)
                    numUnitsShort[:]=np.nan

                    numUnitsLong[0]=0
                    numUnitsLong[longsEntry]=1
                    numUnitsLong[longsExit]=0
                    numUnitsLong=pd.DataFrame(numUnitsLong)
                    numUnitsLong.fillna(method='ffill', inplace=True)

                    numUnitsShort[0]=0
                    numUnitsShort[shortsEntry]=-1
                    numUnitsShort[shortsExit]=0
                    numUnitsShort=pd.DataFrame(numUnitsShort)
                    numUnitsShort.fillna(method='ffill', inplace=True)

                    numUnits=numUnitsLong+numUnitsShort
                    positions=pd.DataFrame(np.tile(numUnits.values, [1, 2]) * ts.add_constant(-hedgeRatio)[:, [1,0]] *df.values) #  [hedgeRatio -ones(size(hedgeRatio))] is the shares allocation, [hedgeRatio -ones(size(hedgeRatio))].*y2 is the dollar capital allocation, while positions is the dollar capital in each ETF.
                    pnl=np.sum((positions.shift().values)*(df.pct_change().values), axis=1) # daily P&L of the strategy
                    ret=pnl/np.sum(np.abs(positions.shift()), axis=1)


                    #plot strategy performance
                    st.info('Strategy Performance')
                    #cumulative return
                    cumret = pd.DataFrame(np.cumprod(1+ret)-1)
                    cumret = cumret.rename(columns={0:'cum_ret'})                
                    fig = plt.figure(figsize=(12,6))
                    plt.plot(cumret)
                    plt.xlabel('Period')
                    st.pyplot(fig)

                    #key metrics
                    st.info('Key Metrics')
                    APR = (np.prod(1+ret)**(252/len(ret))-1)*100
                    SR = np.sqrt(252)*np.mean(ret)/np.std(ret)
                    MDD = np.min(np.cumprod(1+ret) / np.cumprod(1+ret).expanding().max()) -1


                    st.write('Annual Percentage Rate %:',round(APR,2))
                    st.write('Sharpe Ratio:',round(SR,2))
                    st.write('Maximum Drawdown %',round(MDD,2))
                    
                st.success("Done!")

            else:
                st.warning("Ernest P. Chan's words echoed...There is a time and place for everything but data needs to be stationary.")
    except:
        st.error('Insert the right symbol name')
#run in the terminal:
#cd QuantApp
#streamlit run quantapp.py
