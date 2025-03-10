import chromadb
import aiohttp
import asyncio
import os
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chromadb_store")
db_collection = chroma_client.get_or_create_collection(name="google_knowledge")

# Initialize embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Set Together.AI API Key
os.environ["TOGETHER_API_KEY"] = "tgp_v1_EWEOlZXDmLNymaPZWAfxdVIVQlGnUyjU9ugT3mhTO3A"  # Replace with your actual API key
API_KEY = os.getenv("TOGETHER_API_KEY")

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["niche_community"]
posts_collection = db["posts"]
comments_collection = db["comments"]
google_collection = db["Google"]

# Track document count in memory to avoid redundant DB queries
doc_count = len(db_collection.get()["documents"]) if db_collection.get() else 0


async def scrape_google_blogs(rss_url):
    global doc_count
    async with aiohttp.ClientSession() as session:
        async with session.get(rss_url) as response:
            data = await response.text()
            soup = BeautifulSoup(data, "lxml-xml")

            batch_add = []
            for item in soup.find_all("item"):
                title = item.title.text
                link = item.link.text
                description = item.description.text
                content = f"{title} - {description}"

                embedding = embed_model.encode(content).tolist()
                doc_id = f"doc_{doc_count}"
                doc_count += 1
                batch_add.append((doc_id, embedding, content, {"url": link}))

            if batch_add:
                db_collection.add(
                    ids=[x[0] for x in batch_add],
                    embeddings=[x[1] for x in batch_add],
                    documents=[x[2] for x in batch_add],
                    metadatas=[x[3] for x in batch_add],
                )
            print(f"✅ Scraped and stored {len(batch_add)} articles.")


def query_chromadb(user_query):
    query_embedding = embed_model.encode(user_query).tolist()
    results = db_collection.query(query_embeddings=[query_embedding], n_results=1)
    return results["documents"][0][0] if results["documents"] else None


async def generate_response(user_query):
    if not API_KEY:
        return "❌ Error: Missing Together AI API Key."

    relevant_info = query_chromadb(user_query)
    prompt = f"""You are a knowledgeable AI trained in Google-related topics. Answer concisely:

    Information: {relevant_info if relevant_info else "No relevant info found"}
    Question: {user_query}
    Answer:
    """

    url = "https://api.together.xyz/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status != 200:
                return f"❌ Error: {response.status}"
            result = await response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content",
                                                                         "⚠️ Unexpected API response").strip()


async def monitor_community():
    while True:
        google_data = await google_collection.find_one({})
        if not google_data:
            await asyncio.sleep(60)
            continue

        google_keywords = set(
            google_data["areas"] + google_data["technologies"] + [blog["title"] for blog in google_data["blogs"]]
        )

        posts = await posts_collection.find({}, {"_id": 1, "content": 1}).to_list(100)
        comments = await comments_collection.find({}, {"post_id": 1, "comment": 1, "author": 1}).to_list(100)
        commented_post_ids = {comment["post_id"] for comment in comments if comment["author"] == "Google Bot"}

        new_comments = []
        for post in posts:
            if post["_id"] not in commented_post_ids and any(
                    keyword.lower() in post["content"].lower() for keyword in google_keywords):
                response = await generate_response(post["content"])
                new_comments.append(
                    {
                        "post_id": str(post["_id"]),
                        "comment": response,
                        "author": "Google Bot",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

        if new_comments:
            await comments_collection.insert_many(new_comments)
            print(f"✅ Added {len(new_comments)} new comments.")

        await asyncio.sleep(60)


async def start_monitoring():
    rss_feed_url = "https://blog.google/rss/"
    await scrape_google_blogs(rss_feed_url)
    await monitor_community()


if __name__ == "__main__":
    try:
        asyncio.run(start_monitoring())
    except RuntimeError as e:
        print(f"Error: {e}")
