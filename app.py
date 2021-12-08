import streamlit as st
from multiapp import MultiApp
import quantapp
import home
import supportme
#import machlearn
# import your app modules here

from PIL import Image
img = Image.open('stonks.png')
st.set_page_config(page_title='The Smirk',page_icon=img)

app = MultiApp()

st.markdown("""
# The Smirk
""")

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Statistical Arbitrage", quantapp.app)
app.add_app('Support Me',supportme.app)
#app.add_app("Machine Learning for Stocks Prediction",machlearn.app)

# The main app
app.run()
