import pickle
import re
import nltk
import os
import requests
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))
LDA_MODEL_PATH = "D:/SurveySparrow_Assignment/problem1/models/lda_model.pkl"
SENTIMENT_MODEL_PATH = "D:/SurveySparrow_Assignment/problem1/models/sentiment_model.pkl"
with open(LDA_MODEL_PATH, 'rb') as f:
    lda_vectorizer, lda_model = pickle.load(f)
with open(SENTIMENT_MODEL_PATH, 'rb') as f:
    sentiment_model = pickle.load(f)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
TOGETHER_API_KEY = "------"
os.environ["TOGETHER_API_KEY"] = TOGETHER_API_KEY
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    return text
def predict_topic(text):
    processed_text = preprocess_text(text)
    text_vectorized = lda_vectorizer.transform([processed_text])
    topic_distribution = lda_model.transform(text_vectorized)[0]
    predicted_class = topic_distribution.argmax()
    return "Tech" if predicted_class <= 0.5 else "Non-Tech"
def predict_sentiment(text):
    processed_text = preprocess_text(text)
    sentiment = sentiment_model.predict([processed_text])[0]
    return sentiment
def generate_response(user_query, sentiment):
    API_KEY = os.getenv("TOGETHER_API_KEY")
    if not API_KEY:
        return "Error: Missing Together AI API Key."


    if sentiment == "Positive":
        tone = "Friendly & engaging tone"
    elif sentiment == "Neutral":
        tone = "Professional and informative tone"
    elif sentiment == "Negative":
        tone = "Empathetic and encouraging tone"
    else:
        tone = "Neutral tone"

    prompt = f"""You are an AI assistant specializing in Tech-related topics. Answer concisely in a {tone}:

    Question: {user_query}
    Answer:
    """

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"].strip()
        else:
            print(f"API Response: {result}")
            return "Error: Unexpected API response format."

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP Error: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Request Error: {req_err}"
    except Exception as e:
        return f"General Error: {str(e)}"


def interactive_chat():
    print("\nAI Assistant is now live! (Type 'exit' or 'quit' to stop)\n")

    while True:
        user_query = input("Ask a question: ").strip()

        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        topic = predict_topic(user_query)
        if topic != "Tech":
            print("I can only answer Tech-related queries.\n")
            continue

        sentiment = predict_sentiment(user_query)
        print(f"Predicted Sentiment: {sentiment}")

        response = generate_response(user_query, sentiment)
        print(f"AI Reply: {response}\n")


interactive_chat()