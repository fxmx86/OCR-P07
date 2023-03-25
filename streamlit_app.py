# Test Flask API
import streamlit as st
import requests
import numpy as np

text = st.text_input("Text input for sentiment classification API", "It was a quite bad day, poor feeling because I'm sick")

#request_data = {'text': "This movie was badly useless, actors had a bad acting game it's a shame"}
#request_data = {'text': "Today is a good day because I am so in love to this guy"}
#request_data = {'text': "The flight was very nice and one of the stewards was very kind and handsome to me"}
#request_data = {'text': "What a nice restaurant, sushis were very tasteful."}
#request_data = {'text': "It's a bad day, I want to cry because I broke with my girlfriend. It's a poor feeling !"}
request_data = {'text': text}

# URL of the API
url = 'https://fxa-ocrp07-flaskapi.azurewebsites.net:5000/predict_sentiment'

# Send the request containing the text to the API and grab the response r
# Remember r is the json dict containg the sentiment and the probability
r = requests.post(url, params=request_data)

# Display the image array of the mask color image
st.write('API answer', r.json())
