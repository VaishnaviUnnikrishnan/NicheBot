import os
import re
import pickle
import requests
import logging
import time
import nltk
from datetime import datetime, timedelta
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
SLACK_BOT_USER_ID = "U08ES91F37Y"  # Set your bot's user ID directly
if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN or not TOGETHER_API_KEY:
    logging.error(" Missing API tokens. Ensure the .env file is set up correctly.")
    exit(1)

client = WebClient(token=SLACK_BOT_TOKEN)


LDA_MODEL_PATH = "D:/SurveySparrow_Assignment/problem1/models/lda_model.pkl"
SENTIMENT_MODEL_PATH = "D:/SurveySparrow_Assignment/problem1/models/sentiment_model.pkl"

try:
    with open(LDA_MODEL_PATH, "rb") as f:
        lda_vectorizer, lda_model = pickle.load(f)

    with open(SENTIMENT_MODEL_PATH, "rb") as f:
        sentiment_model = pickle.load(f)

    logging.info("Models loaded successfully.")
except Exception as e:
    logging.error(f"Error loading models: {str(e)}")
    exit(1)


embed_model = SentenceTransformer("all-MiniLM-L6-v2")


processed_messages = set()

MESSAGE_EXPIRATION_TIME = timedelta(minutes=1)
message_timestamps = {}


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = " ".join([word for word in text.split() if word not in STOPWORDS])
    return text


def predict_topic(text):
    processed_text = preprocess_text(text)
    text_vectorized = lda_vectorizer.transform([processed_text])
    topic_distribution = lda_model.transform(text_vectorized)[0]
    return "Tech" if topic_distribution.argmax() <= 0.5 else "Non-Tech"


def predict_sentiment(text):
    processed_text = preprocess_text(text)
    return sentiment_model.predict([processed_text])[0]


def generate_response(user_query, sentiment):
    tone_map = {
        "Positive": "Friendly & engaging tone",
        "Neutral": "Professional and informative tone",
        "Negative": "Empathetic and encouraging tone",
    }
    tone = tone_map.get(sentiment, "Neutral tone")

    prompt = f"""You are an AI assistant specializing in Tech-related topics. Answer concisely in a {tone}:

    Question: {user_query}
    Answer:
    """

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return "Error: Unexpected API response format."

    except requests.exceptions.RequestException as e:
        return f" Request Error: {str(e)}"

# Handle Slack Messages
def handle_message(event_data):
    if "text" in event_data and "subtype" not in event_data:
        user_query = event_data["text"]
        channel_id = event_data["channel"]
        message_ts = event_data.get("ts")
        user_id = event_data.get("user")


        if user_id == SLACK_BOT_USER_ID:
            logging.info(f"Ignoring own message: {user_query}")
            return


        if message_ts in processed_messages:
            logging.info(f"Duplicate message detected, ignoring: {user_query}")
            return


        processed_messages.add(message_ts)
        message_timestamps[message_ts] = datetime.now()  # Store the timestamp

        logging.info(f"Received message in channel {channel_id}: {user_query}")

        topic = predict_topic(user_query)
        if topic != "Tech":
            response_text = "I can only answer Tech-related queries."
        else:
            sentiment = predict_sentiment(user_query)
            response_text = generate_response(user_query, sentiment)

        client.chat_postMessage(channel=channel_id, text=response_text)
        logging.info(f"Sent response: {response_text}")


        time.sleep(1)


def cleanup_processed_messages():
    current_time = datetime.now()
    expired_messages = [ts for ts, timestamp in message_timestamps.items() if current_time - timestamp > MESSAGE_EXPIRATION_TIME]
    for ts in expired_messages:
        processed_messages.remove(ts)
        del message_timestamps[ts]

def process_events(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        event_data = req.payload["event"]

        logging.info(f"Received event: {event_data}")


        client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))


        handle_message(event_data)

if __name__ == "__main__":
    try:
        socket_client = SocketModeClient(app_token=SLACK_APP_TOKEN, web_client=client)
        socket_client.socket_mode_request_listeners.append(process_events)
        logging.info("Slack bot is now running...")

        socket_client.connect()

        while True:
            cleanup_processed_messages()
            time.sleep(10)

    except Exception as e:
        logging.error(f"Slack bot error: {str(e)}")