import chromadb
from chromadb.config import Settings
from config import get_settings
import os

settings = get_settings()

# Initialize ChromaDB client
def get_chroma_client():
    """Get or create ChromaDB client"""
    # Create directory if doesn't exist
    os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
    
    client = chromadb.PersistentClient(
        path=settings.CHROMA_PERSIST_DIRECTORY
    )
    return client

def get_or_create_collection():
    """Get or create conversations collection"""
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name="scam_conversations",
        metadata={"hnsw:space": "cosine"}
    )
    return collection

def store_conversation(session_id: str, conversation_text: str, metadata: dict):
    """Store conversation in ChromaDB"""
    collection = get_or_create_collection()
    
    collection.add(
        documents=[conversation_text],
        metadatas=[metadata],
        ids=[session_id]
    )

def search_similar_scams(query_text: str, n_results: int = 3):
    """Search for similar scam conversations"""
    collection = get_or_create_collection()
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return results
