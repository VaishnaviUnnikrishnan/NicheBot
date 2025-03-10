import json
import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
nltk.download('stopwords')
STOPWORDS=set(stopwords.words('english'))
LDA_DATA_PATH=r"D:\SurveySparrow_Assignment\problem1\webscraping_model\data\scraped_data.json"
SENTIMENT_DATA_PATH=r"D:\SurveySparrow_Assignment\problem1\topic_modelling\train.csv"
def load_lda_data(a):
    with open(a,'r',encoding='utf-8') as b:
        c=json.load(b)
    d=[]
    e=[]
    for f,g in c.items():
        for h in g:
            if 'question' in h and 'topic' in h:
                d.append(h['question'])
                e.append(h['topic'].lower())
    return d,e
def preprocess_text(i):
    i=i.lower()
    i=re.sub(r'[^a-zA-Z]',' ',i)
    i=' '.join([j for j in i.split() if j not in STOPWORDS])
    return i
def load_sentiment_data(k):
    l=pd.read_csv(k)
    l.dropna(inplace=True)
    l['processed_text']=l['text'].apply(preprocess_text)
    return l
def train_lda_model(m,n):
    o={"Programming","AI","Technology","Data"}
    p=[1 if any(q in r for q in o) else 0 for r in n]
    s=CountVectorizer(max_features=1000)
    t=s.fit_transform(m)
    u=LatentDirichletAllocation(n_components=2,random_state=42)
    u.fit(t)
    with open('lda_model.pkl','wb') as v:
        pickle.dump((s,u),v)
    print("LDA Model saved as lda_model.pkl")
def train_sentiment_model(w):
    x_train,x_test,y_train,y_test=train_test_split(w['processed_text'],w['sentiment'],test_size=0.2,random_state=42)
    y=TfidfVectorizer(max_features=5000)
    z=MultinomialNB()
    aa=make_pipeline(y,z)
    aa.fit(x_train,y_train)
    ab=aa.predict(x_test)
    ac=accuracy_score(y_test,ab)
    print(f"Sentiment Model Accuracy: {ac:.2f}")
    with open('sentiment_model.pkl','wb') as ad:
        pickle.dump(aa,ad)
    print("Sentiment Model saved as sentiment_model.pkl")
if __name__=="__main__":
    ae,af=load_lda_data(LDA_DATA_PATH)
    ae=[preprocess_text(ag) for ag in ae]
    train_lda_model(ae,af)
    ah=load_sentiment_data(SENTIMENT_DATA_PATH)
    train_sentiment_model(ah)