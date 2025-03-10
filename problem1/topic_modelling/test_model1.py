import pickle
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
STOPWORDS=set(stopwords.words('english'))
with open('problem1/models/lda_model.pkl','rb') as a:
    b,c=pickle.load(a)
with open('problem1/models/sentiment_model.pkl','rb') as d:
    e=pickle.load(d)
def preprocess_text(f):
    f=f.lower()
    f=re.sub(r'[^a-zA-Z]',' ',f)
    f=' '.join([g for g in f.split() if g not in STOPWORDS])
    return f
def predict_topic(h):
    i=preprocess_text(h)
    j=b.transform([i])
    k=c.transform(j)[0]
    l=k.argmax()
    return "Tech" if l<=0.5 else "Non-Tech"
def predict_sentiment(m):
    n=preprocess_text(m)
    o=e.predict([n])[0]
    return o
if __name__=="__main__":
    while True:
        p=input("\nEnter text (or type 'exit' to quit): ").strip()
        if p.lower()=='exit':
            print("Exiting...")
            break
        q=predict_topic(p)
        r=predict_sentiment(p)
        print(f"\nPredicted Topic: {q}")
        print(f"Predicted Sentiment: {r}")