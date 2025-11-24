"""
Vector Database module for LinkedInsight using ChromaDB.

This module provides functionality to store and query job embeddings
for semantic similarity search.
"""

import chromadb
from typing import List, Dict, Any, Optional
from app.core.embeddings import embed_text


# Initialize ChromaDB client (in-memory for now)
# Using EphemeralClient for true in-memory storage (no persistence)
# This is simpler and doesn't require file system access
client = chromadb.EphemeralClient()

# Collection name for job embeddings
COLLECTION_NAME = "job_embeddings"

# Get or create the collection with cosine distance metric
# Cosine distance is ideal for semantic similarity search
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}  # Use cosine distance
)


def add_job_embedding(id: str, text: str, metadata: Dict[str, Any]) -> bool:
    """
    Add a job embedding to the vector store.
    
    This function generates an embedding for the provided text using OpenAI's
    embedding model and stores it in ChromaDB along with associated metadata.
    
    Args:
        id (str): Unique identifier for the job (e.g., job posting ID).
                  Must be unique within the collection.
        text (str): The text content to embed (e.g., job description, title).
                   Should not be empty.
        metadata (Dict[str, Any]): Additional metadata to store with the embedding.
                                   Common fields: title, company, location, etc.
    
    Returns:
        bool: True if the embedding was successfully added, False otherwise.
    
    Raises:
        ValueError: If text is empty or id is invalid.
        Exception: If embedding generation or storage fails.
    
    Example:
        >>> metadata = {
        ...     "title": "Software Engineer",
        ...     "company": "Tech Corp",
        ...     "location": "Seattle, WA"
        ... }
        >>> add_job_embedding("job_123", "Looking for a Python developer...", metadata)
        True
    """
    if not id or not isinstance(id, str):
        raise ValueError("ID must be a non-empty string")
    
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary")
    
    try:
        # Generate embedding for the text
        embedding = embed_text(text)
        
        if not embedding:
            raise ValueError("Failed to generate embedding for the provided text")
        
        # Add the embedding to ChromaDB
        # ChromaDB expects: ids (list), embeddings (list of lists), documents (list), metadatas (list of dicts)
        collection.add(
            ids=[id],
            embeddings=[embedding],
            documents=[text],  # Store original text for retrieval
            metadatas=[metadata]
        )
        
        return True
    
    except Exception as e:
        # Log error in production (add logging later)
        print(f"Error adding job embedding: {str(e)}")
        raise


def query_similar_jobs(text: str, n: int = 5, filter_metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Query the vector store for jobs similar to the provided text.
    
    This function embeds the query text and searches for the most similar
    job embeddings using cosine similarity. Returns the top n most similar
    results with their metadata and similarity scores.
    
    Args:
        text (str): The query text to search for (e.g., "Python developer role").
                    Should not be empty.
        n (int, optional): Number of similar jobs to return. Defaults to 5.
                          Must be a positive integer.
        filter_metadata (Dict[str, Any], optional): Optional metadata filters to apply.
                                                    Only jobs matching these filters will be returned.
                                                    Example: {"location": "Seattle, WA"}
    
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing:
            - id (str): The unique identifier of the job
            - text (str): The original text/document
            - metadata (Dict[str, Any]): The stored metadata for the job
            - distance (float): The cosine distance (lower = more similar)
            - similarity (float): The cosine similarity score (higher = more similar)
                                 Calculated as 1 - distance
    
    Raises:
        ValueError: If text is empty or n is not a positive integer.
        Exception: If embedding generation or query fails.
    
    Example:
        >>> results = query_similar_jobs("Python software engineer", n=3)
        >>> for result in results:
        ...     print(f"{result['metadata']['title']} - Similarity: {result['similarity']:.3f}")
    """
    if not text or not text.strip():
        raise ValueError("Query text cannot be empty")
    
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer")
    
    try:
        # Generate embedding for the query text
        query_embedding = embed_text(text)
        
        if not query_embedding:
            raise ValueError("Failed to generate embedding for the query text")
        
        # Query the collection
        # where parameter is used for metadata filtering
        query_results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n,
            where=filter_metadata if filter_metadata else None
        )
        
        # Format results into a more usable structure
        results = []
        
        # ChromaDB returns results in lists (one per query)
        if query_results['ids'] and len(query_results['ids'][0]) > 0:
            ids = query_results['ids'][0]
            documents = query_results['documents'][0]
            metadatas = query_results['metadatas'][0]
            distances = query_results['distances'][0]
            
            for i in range(len(ids)):
                result = {
                    'id': ids[i],
                    'text': documents[i],
                    'metadata': metadatas[i] if metadatas[i] else {},
                    'distance': distances[i],
                    'similarity': 1 - distances[i]  # Convert distance to similarity
                }
                results.append(result)
        
        return results
    
    except Exception as e:
        # Log error in production (add logging later)
        print(f"Error querying similar jobs: {str(e)}")
        raise


def delete_job_embedding(id: str) -> bool:
    """
    Delete a job embedding from the vector store.
    
    Args:
        id (str): The unique identifier of the job to delete.
    
    Returns:
        bool: True if the job was successfully deleted, False otherwise.
    """
    try:
        collection.delete(ids=[id])
        return True
    except Exception as e:
        print(f"Error deleting job embedding: {str(e)}")
        return False


def get_collection_stats() -> Dict[str, Any]:
    """
    Get statistics about the job embeddings collection.
    
    Returns:
        Dict[str, Any]: Dictionary containing collection statistics:
            - count (int): Number of embeddings in the collection
    """
    count = collection.count()
    return {
        'count': count,
        'collection_name': COLLECTION_NAME
    }

