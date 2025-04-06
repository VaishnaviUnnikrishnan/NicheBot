import nltk
import torch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_community.llms import Ollama
from nltk.sentiment import SentimentIntensityAnalyzer

# Download sentiment lexicon if not already
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# Load vectorstore and retriever
embedding_model = "all-MiniLM-L6-v2"
vectorstore = Chroma(
    persist_directory="D:/NicheBot/data/oracle_scraped_data",
    embedding_function=HuggingFaceEmbeddings(model_name=embedding_model)
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Function to analyze sentiment
def analyze_sentiment(text):
    score = sia.polarity_scores(text)["compound"]
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"

# Setup LLaMA 3 from Ollama
llm = Ollama(model="llama3.2")

# Conversational Prompt Template
prompt_template = PromptTemplate.from_template("""
You are a helpful and friendly Oracle-savvy assistant. Speak naturally, like you're talking to a colleague.
Given the following context, answer the user's question conversationally.

User's Question: {query}
Relevant Info: {context}
Sentiment Summary: {sentiments}

Respond like a helpful human who knows Oracle well. Keep it conversational.
""")

# Generate response from retriever + LLM
def generate_response(query):
    docs = retriever.get_relevant_documents(query)
    contexts = [doc.page_content for doc in docs]
    sentiments = [analyze_sentiment(text) for text in contexts]

    prompt = prompt_template.format(
        query=query,
        context="\n".join(contexts),
        sentiments=", ".join(sentiments)
    )

    return llm.invoke(prompt)

if __name__ == "__main__":
    print("Hey there! I’m LimeLight.Your go-to Oracle assistant!.")
    print("Ask me anything about Oracle.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Limelight: Alright, talk to you later!")
            break
        elif user_input.lower() in ["hi", "hello", "hey"]:
            print("Limelight: Hi there! What would you like to know about Oracle today?")
            continue

        answer = generate_response(user_input)
        print("\nBot:", answer.strip(), "\n")
