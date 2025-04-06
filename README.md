# LimeLight 

## Overview
**LimeLight** is an intelligent, autonomous assistant integrated into a community platform. It focuses on detecting, retrieving, and responding to user-generated content related to **Oracle**, its products, and subsidiaries using a Retrieval-Augmented Generation (RAG) pipeline powered by **LangChain**, **ChromaDB**, and **LLaMA 3**.

This project aims to make community engagement more meaningful and efficient by automating informative replies and offering sentiment-aware context.

---

## Features

### 1. Oracle RAG Assistant (LimeLight Bot)
- Detects **Oracle-related content** using keyword filtering and semantic similarity.
- Retrieves relevant information from a **ChromaDB vector store**.
- Uses **LLaMA 3 (via Ollama)** to generate context-aware replies using LangChain's RAG pipeline.
- Performs  **sentiment analysis** to enrich response tone.
- Ensures high-quality responses only for verified Oracle-related topics.

### 2. Post Interaction and Auto-Commenting
- When a **user creates a post**, the system:
  - Checks if it's Oracle-related.
  - If yes, triggers the `generate_response()` function from `bot.py`.
  - Inserts a **comment** from LimeLight into the database and displays it on the post thread.
- Comments are tagged as authored by "LimeLight" and timestamped.

### 3. FastAPI Community Platform
- Built using **FastAPI**, **MongoDB**, and **Jinja2**.
- Routes for user posts and viewing threads.
- Lightweight frontend for displaying posts and bot replies.
- Modular design (`main.py`, `response.py`, `bot.py`) to separate concerns.

---

## Machine Learning / NLP Used

### 1. RAG Pipeline
- Uses **ChromaDB** to store and retrieve Oracle data chunks.
- Embeds data using **HuggingFace sentence transformers**.
- Queries are processed via **LangChain** for:
  - Similarity search.
  - Augmented response generation using **LLaMA 3**.

### 2. Oracle Relevance Detection
- Checks for keywords like *oracle*, *oci*, *fusion apps*, *netsuite*, etc.
- Planned enhancement: Use an LLM classifier for better accuracy.

### 3. Sentiment Analysis *(Planned)*
- Analyze user tone (positive, negative, neutral).
- Adapt LimeLight’s responses to be empathetic or supportive when needed.

---

## Tech Stack

| Component       | Technology                        |
|----------------|------------------------------------|
| **Backend**     | FastAPI                           |
| **Database**    | MongoDB (via `motor`)             |
| **Frontend**    | HTML, CSS, Jinja2                 |
| **LLM**         | LLaMA 3 via Ollama                |
| **RAG**         | LangChain + ChromaDB              |
| **Embeddings**  | HuggingFace Transformers          |
| **Future ML**   | Sentiment Analysis with Transformers |

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/limelight-oracle-bot.git
   cd limelight-oracle-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

5. Ensure LLaMA 3 is running locally via Ollama:
   ```bash
   ollama run llama3
   ```

6. Visit the app at:
   ```
   http://localhost:8000
   ```

---


---

## License
This project is licensed under the MIT License.

---

## Contact
For any questions or collaborations, reach out to:  
📧 **v.ukrishnan8@gmail.com**

---

## Screenshots
![Screenshot 2025-04-06 110540](https://github.com/user-attachments/assets/85214745-5ed5-41c4-af20-16b0430b5379)

![Screenshot 2025-04-06 110619](https://github.com/user-attachments/assets/ed37ee78-eb46-4aea-8aff-4a0cf02f4da8)

![Screenshot 2025-04-06 110626](https://github.com/user-attachments/assets/e84c974f-4efc-4a25-8960-251abff5eb33)

![Screenshot 2025-04-06 113155](https://github.com/user-attachments/assets/d155afad-9bc2-4b06-9e5e-7b147e92790e)

![image](https://github.com/user-attachments/assets/189dc233-c935-4732-b487-1df2220b2976)




