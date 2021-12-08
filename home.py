import streamlit as st

def app():
    st.title('Welcome')

    st.write('To this page. The Smirk is a Web page App that allows user, that doesn’t have a particular coding skill, to do backtesting their strategy')
    
    link = '[TheSmirk](https://thesmile.herokuapp.com/)'
    st.subheader("Second Part:")
    st.markdown(link, unsafe_allow_html=True)
