# LimeLight


---

```markdown
# 🧠 LimeLight Oracle Assistant Bot

LimeLight is an AI-powered assistant integrated into a niche community platform. It automatically analyzes user-generated posts related to Oracle, its products, and subsidiaries, and replies with helpful insights using a Retrieval-Augmented Generation (RAG) pipeline.

---

## 🚀 Features

### ✅ RAG-based Oracle Assistant
- Built using **LangChain** + **ChromaDB**.
- Uses **LLaMA 3** (via Ollama) as the base LLM.
- Performs:
  - Oracle relevance detection.
  - Embedding + similarity search.
  - Sentiment analysis (planned).
  - Custom responses generated via RAG.

### ✅ Community Bot Integration
- FastAPI-based web platform for niche tech communities.
- Automatically replies to relevant Oracle-related posts using `LimeLight` bot.
- Bot replies stored in MongoDB and rendered alongside user comments.

### ✅ Post Workflow
1. User creates a post.
2. Post is checked for Oracle relevance.
3. If relevant:
   - Sent to `generate_response()` function from `bot.py`.
   - LimeLight generates and stores a comment.
4. The comment appears in the post’s thread.

---

## 🛠️ Tech Stack

| Component       | Tech                                  |
|----------------|----------------------------------------|
| **Backend**     | FastAPI                               |
| **Database**    | MongoDB (via `motor`)                 |
| **LLM**         | LLaMA 3 (Ollama local instance)       |
| **Embeddings**  | HuggingFace + ChromaDB vector store   |
| **RAG Tooling** | LangChain                             |
| **Frontend**    | Jinja2 templating (HTML/CSS/JS)       |

---

## 🧩 File Structure

```
├── bot.py                 # RAG logic to generate responses
├── response.py            # Auto-commenting logic for LimeLight
├── main.py                # FastAPI app with post & comment routes
├── static/                # CSS, JS, assets
├── templates/             # HTML templates
├── data/                  # Scraped Oracle data (PDFs, JSON, etc.)
└── README.md              # This file
```

---

## 🧠 Example Bot Logic

### is_oracle_related()
```python
def is_oracle_related(text: str) -> bool:
    oracle_keywords = ["oracle", "oci", "fusion apps", "netsuite", "larry ellison"]
    return any(keyword in text.lower() for keyword in oracle_keywords)
```

### Comment Insertion
```python
comment_data = {
    "post_id": post_id,
    "comment": bot_reply,
    "author": "LimeLight",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
await comments_collection.insert_one(comment_data)
```

---

## 🔮 Planned Features

- 💬 Auto-comment on **user comments**, not just posts.
- 📊 Perform **sentiment analysis** to add context to LimeLight replies.
- 🗂️ Dashboard to view bot analytics (number of replies, likes, etc).
- 🧪 Test UI/UX survey for feedback on LimeLight-generated comments.

---

## 🏁 Setup Instructions

1. **Start ChromaDB and Ollama**
   ```bash
   ollama run llama3
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run FastAPI App**
   ```bash
   uvicorn main:app --reload
   ```

4. **Visit**
   ```
   http://localhost:8000
   ```

---

## 🤖 Bot Identity

- **Name**: LimeLight
- **Purpose**: Serve accurate and insightful information on Oracle tech, tools, products, and its ecosystem.
- **Mode**: Autonomous — responds only to posts that contain Oracle-relevant content.

---

## 📄 License

MIT License

---

## 💡 Credits

Developed by Vaishnavi Unnikrishnan — integrating LLMs into intelligent community tools.
```
