# embed.py

import os
import json
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document  # updated for langchain-core

DATA_DIR = "data"
CHROMA_DIR = "data/oracle_scraped_data"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Initialize embedding model
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Collect and load documents
all_documents = []

def load_text_file(filepath):
    loader = TextLoader(filepath, encoding="utf-8")
    return loader.load()

def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = json.load(f)
        docs = []
        if isinstance(content, list):
            for item in content:
                text = json.dumps(item) if isinstance(item, dict) else str(item)
                docs.append(Document(page_content=text))
        elif isinstance(content, dict):
            docs = [Document(page_content=json.dumps(content))]
        return docs

# Walk through all files in data/
for root, _, files in os.walk(DATA_DIR):
    for file in files:
        path = os.path.join(root, file)
        if file.endswith(".txt"):
            try:
                all_documents.extend(load_text_file(path))
            except Exception as e:
                print(f"⚠️ Skipping file due to error: {path}\n{e}")
        elif file.endswith(".json"):
            all_documents.extend(load_json_file(path))

# Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(all_documents)

# Store in Chroma
vectorstore = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory=CHROMA_DIR
)
vectorstore.persist()

print(f"Embedded {len(split_docs)} chunks into ChromaDB at '{CHROMA_DIR}'")
