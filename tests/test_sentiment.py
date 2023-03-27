import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
#from app import *
from app import predict_sentiment

negative_text = "It's a bad day, I want to cry because I broke with my girlfriend. It's a poor feeling !"
positive_text = "What a nice restaurant, sushis were very tasteful."
def test_negative():
    assert predict_sentiment(negative_text)[0] == "negative"

def test_positive():
    assert predict_sentiment(positive_text)[0] == "positive"
