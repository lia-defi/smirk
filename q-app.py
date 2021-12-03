import streamlit as st
from multiapp import MultiApp
import quantapp
import home
import supportme
# import your app modules here

app = MultiApp()

st.markdown("""
# Multi-Page App
""")

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Statistical Arbitrage", quantapp.app)
app.add_app('Support Me',supportme.app)

# The main app
#app.run()
