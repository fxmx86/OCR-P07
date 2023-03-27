# Access via http://fxa-ocrp07-flaskapi.azurewebsites.net:5000

# Defining a function to save/restore objects in/from the zip file FileZip. Objects contains the objects list.
import pandas as pd
import os.path, zipfile, pickle

def zip_save_restore(FileZip: str, Objects: list[]=[], Format: str="pickle", *args, **kwargs):
    """ Depending on the zip file existence, this function will :
        - save all listed objects in a small zip file, if not already done.
        - restore inexistent objects from pickle/CSV files in zip file, with *args, **kwargs if available.
        ** More work to be done to get rid of globals(), with objects in a dictionary ? **
    """
    
    ext = ""; objs = []
    if not os.path.isfile(FileZip):
        with zipfile.ZipFile(FileZip, mode="w", compression=zipfile.ZIP_BZIP2) as zip:
            for obj in Objects:
                if Format == "pickle" :
                    with open(obj, 'wb') as handle: pickle.dump(globals()[obj], handle, protocol=-1)
                if Format != "pickle" : Format = "CSV"; ext = ".csv"; globals()[obj].to_csv(obj+ext)
                zip.write(obj+ext); os.remove(obj+ext); print (obj + " : object saved (" + Format + ")"); ext = ""
        return Objects
    else:
        with zipfile.ZipFile(FileZip, mode="r") as zip:
            for file in zip.infolist():
                file = file.filename; obj = file.replace(".csv", "").replace(".", "")
                msg = "object already exist or not in listed Objects"
                if obj not in globals() and (Objects == [] or obj in Objects):
                    if file.find(".csv") >= 0 or Format != "pickle" :
                        msg = "(CSV W global params, if existent)"
                        try:
                            args1 = obj + "_args"; kwargs1 = obj + "_kwargs"
                            if args1 in globals() and kwargs1 in globals():
                                msg = "(CSV W unique params)"
                                globals()[obj] = pd.read_csv(zip.open(file), *globals()[args1], **globals()[kwargs1])
                            else:
                                globals()[obj] = pd.read_csv(zip.open(file), *args, **kwargs)
                        except Exception as ex:
                            print('ERROR : ', ex); msg = "or not (ERROR above !)"
                    else :
                        msg = "(pickle)"; globals()[obj] = pd.read_pickle(zip.open(file), *args, **kwargs)
                        if isinstance(globals()[obj], pd.DataFrame): globals()[obj].sort_index(inplace=True)
                    msg = "object restored " + msg
                objs.append(obj); print (obj + " : " + msg)
        return objs

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, request, jsonify

MAX_SEQUENCE_LENGTH = 50

# loading the model and the tokenizer from the best configuration trained
best_model = load_model("./bidir_LSTM_raw_fasttext.h5")
zip_save_restore("TokenDict.zip", ["TOKENIZER_DICT"])
tokenizer = TOKENIZER_DICT["raw"]

def predict_sentiment(tweet):
    index_sequence = pad_sequences(tokenizer.texts_to_sequences([tweet]), maxlen=MAX_SEQUENCE_LENGTH, padding='post')
    probability_score = best_model.predict(index_sequence)[0][0]

    sentiment = "negative" if probability_score < 0.5 else "positive"
    
    return sentiment, probability_score

"""text_to_explain = ["It was a quite bad day, poor feeling because I'm sick",
                   "This movie was badly useless, actors had a bad acting game it's a shame",
                   "Today is a good day because I am so in love to this guy",
                   "The flight was very nice and one of the stewards was very kind and handsome to me"]

for tweet in text_to_explain:
    print(tweet, ":", predict_sentiment(tweet))"""

app = Flask(__name__)

# Route to the API
@app.route("/predict_sentiment", methods=["POST"])
def predict():
    # Get the text included in the request and process the text in order to get the sentiment
    text = request.args['text']
    results = predict_sentiment(text)

    return jsonify(text=text, sentiment=results[0], probability=str(results[1]))

# Route to the welcome page
@app.route("/")
def home():
    return "Hello, this is a sentiment classification API (access on /predict_sentiment) !"

#if __name__ == "__main__":
#    app.run(debug=True)
