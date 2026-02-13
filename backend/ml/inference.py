import pickle 
import re
import os

###find the base directory of the current file to load the model and vectorizer
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "artifacts", "risk_model.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "artifacts", "tfidf.pkl")
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, "artifacts", "label_encoder.pkl")

###load the model 
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)
    
with open(TFIDF_PATH, "rb") as f:
    tfidf=pickle.load(f)
    
with open(LABEL_ENCODER_PATH, "rb") as f:
    lable_encoder=pickle.load(f)
    
###text preprocessing 

def clean_text(text):
    text=text.lower()
    text=re.sub(r"[^a-z\s]", "", text)
    text=re.sub(r"\s+", " ", text)
    return text.strip()


###Risk prediction 
def predict_risk(text:str)->str:
    cleaned_text=clean_text(text)
    
    ##convert text into numeric values 
    vector = tfidf.transform([cleaned_text])
    
    ##predict class label
    prediction = model.predict(vector)[0]
    
    ###return probablity for each class 
    try:
      confidence = model.predict_proba(vector).max()
      confidence = round(float(confidence), 2)
    except:
      confidence = None
      
      
    return {
        "risk": lable_encoder.inverse_transform([prediction])[0],
        "confidence": confidence
    }


