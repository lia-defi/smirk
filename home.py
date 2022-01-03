import streamlit as st
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
def app():
    st.title('Welcome')

    st.write('To this page. The Smirk is a Web page App that allows user, that doesn’t have a particular coding skill, to do backtesting their strategy')
    
    link = '[TheSmile](https://thesmile.herokuapp.com/)'
    st.subheader("Second Part:")
    st.markdown(link, unsafe_allow_html=True)
