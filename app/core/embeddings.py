"""
Embeddings Service for LinkedInsight.

This module provides text embedding functionality using OpenAI's embedding models.
Embeddings are used to convert text into vector representations for semantic search
and similarity matching in the vector database.

TODO: Add batching and caching for improved performance.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_MODEL = "text-embedding-3-large"

def embed_text(text: str) -> list:
    """
    Generate an embedding vector for a given text.
    """
    if not text or text.strip() == "":
        return []

    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return resp.data[0].embedding

