"""
Jobs Router for LinkedInsight API.

This router provides endpoints for:
- Scraping and ingesting job postings
- Semantic job matching using vector search
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.core.pipeline import scrape_job_postings, ingest_jobs_into_vector_db
from app.db.vector_store import query_similar_jobs

router = APIRouter(prefix="/jobs", tags=["jobs"])


class ScrapeJobsRequest(BaseModel):
    """Request model for scraping jobs."""
    query: str = Field(..., description="Job search query (e.g., 'software engineer', 'data scientist')")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of jobs to scrape (1-100)")


class ScrapeJobsResponse(BaseModel):
    """Response model for scraping jobs."""
    query: str
    scraped_count: int
    ingestion_summary: Dict[str, Any]
    message: str


class JobMatchResponse(BaseModel):
    """Response model for a single job match."""
    id: str
    title: str
    company: str
    location: str
    similarity: float
    distance: float
    url: str
    programming_languages: str
    technical_skills: str


class MatchJobsResponse(BaseModel):
    """Response model for job matching endpoint."""
    query_text: str
    matches: List[JobMatchResponse]
    count: int


@router.post("/scrape", response_model=ScrapeJobsResponse)
def scrape_and_ingest_jobs(request: ScrapeJobsRequest):
    """
    Scrape job postings from public job boards and ingest them into the vector database.
    
    This endpoint performs a complete pipeline:
    1. Scrapes job postings from publicly accessible job boards (e.g., Indeed)
    2. Extracts skills and requirements from job descriptions
    3. Ingests jobs into the vector database with embeddings
    
    **Request Body:**
    ```json
    {
        "query": "software engineer",
        "limit": 15
    }
    ```
    
    **Returns:**
    - `query` (str): The search query used
    - `scraped_count` (int): Number of jobs successfully scraped
    - `ingestion_summary` (dict): Summary of ingestion process:
        - `total_jobs` (int): Total jobs to ingest
        - `processed` (int): Successfully processed
        - `failed` (int): Failed to process
        - `errors` (List[str]): Error messages for failed jobs
    - `message` (str): Human-readable summary
    
    **Example:**
    ```bash
    POST /jobs/scrape
    {
        "query": "Python developer",
        "limit": 10
    }
    ```
    
    **Response:**
    ```json
    {
        "query": "Python developer",
        "scraped_count": 10,
        "ingestion_summary": {
            "total_jobs": 10,
            "processed": 10,
            "failed": 0,
            "errors": []
        },
        "message": "Successfully scraped 10 jobs and processed 10 into vector database"
    }
    ```
    """
    try:
        # Validate input
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        query = request.query.strip()
        
        # Scrape job postings
        print(f"Scraping jobs for query: '{query}' with limit: {request.limit}")
        jobs = scrape_job_postings(query, limit=request.limit)
        
        if not jobs:
            return ScrapeJobsResponse(
                query=query,
                scraped_count=0,
                ingestion_summary={
                    "total_jobs": 0,
                    "processed": 0,
                    "failed": 0,
                    "errors": []
                },
                message=f"No jobs found for query: '{query}'"
            )
        
        # Ingest into vector database
        print(f"Ingesting {len(jobs)} jobs into vector database...")
        ingestion_result = ingest_jobs_into_vector_db(jobs)
        
        # Create response message
        if ingestion_result['processed'] == ingestion_result['total_jobs']:
            message = f"Successfully scraped {len(jobs)} jobs and processed {ingestion_result['processed']} into vector database"
        else:
            message = f"Scraped {len(jobs)} jobs. Processed {ingestion_result['processed']}, {ingestion_result['failed']} failed"
        
        return ScrapeJobsResponse(
            query=query,
            scraped_count=len(jobs),
            ingestion_summary=ingestion_result,
            message=message
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error scraping or ingesting jobs: {str(e)}"
        )


@router.get("/match", response_model=MatchJobsResponse)
def match_jobs(
    text: str = Query(..., description="Query text to find similar jobs (e.g., 'backend developer', 'Python engineer')"),
    n: int = Query(default=5, ge=1, le=20, description="Number of similar jobs to return (1-20)")
):
    """
    Find jobs similar to the provided query text using semantic search.
    
    This endpoint uses vector embeddings to find jobs that are semantically similar
    to the query text, even if they don't contain exact keyword matches. This enables
    intelligent job matching based on meaning rather than just keywords.
    
    **Query Parameters:**
    - `text` (str): Query text describing the type of job you're looking for
    - `n` (int, optional): Number of results to return (default: 5, max: 20)
    
    **Returns:**
    - `query_text` (str): The query text used
    - `matches` (List[JobMatchResponse]): List of matching jobs, each containing:
        - `id` (str): Unique job identifier
        - `title` (str): Job title
        - `company` (str): Company name
        - `location` (str): Job location
        - `similarity` (float): Similarity score (0-1, higher is more similar)
        - `distance` (float): Cosine distance (lower is more similar)
        - `url` (str): URL to the job posting
        - `programming_languages` (str): Comma-separated programming languages
        - `technical_skills` (str): Comma-separated technical skills
    - `count` (int): Number of matches returned
    
    **Example:**
    ```bash
    GET /jobs/match?text=backend developer&n=5
    ```
    
    **Response:**
    ```json
    {
        "query_text": "backend developer",
        "matches": [
            {
                "id": "abc123",
                "title": "Senior Backend Engineer",
                "company": "Tech Corp",
                "location": "Seattle, WA",
                "similarity": 0.89,
                "distance": 0.11,
                "url": "https://...",
                "programming_languages": "Python, JavaScript",
                "technical_skills": "Django, PostgreSQL, AWS"
            }
        ],
        "count": 5
    }
    ```
    """
    try:
        if not text or not text.strip():
            raise HTTPException(status_code=400, detail="Query text cannot be empty")
        
        query_text = text.strip()
        
        # Query similar jobs from vector database
        results = query_similar_jobs(query_text, n=n)
        
        # Format results
        matches = []
        for result in results:
            metadata = result.get('metadata', {})
            match = JobMatchResponse(
                id=result.get('id', ''),
                title=metadata.get('title', 'N/A'),
                company=metadata.get('company', 'N/A'),
                location=metadata.get('location', 'N/A'),
                similarity=round(result.get('similarity', 0.0), 4),
                distance=round(result.get('distance', 1.0), 4),
                url=metadata.get('url', ''),
                programming_languages=metadata.get('programming_languages', ''),
                technical_skills=metadata.get('technical_skills', '')
            )
            matches.append(match)
        
        return MatchJobsResponse(
            query_text=query_text,
            matches=matches,
            count=len(matches)
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error matching jobs: {str(e)}"
        )


@router.get("/stats")
def get_job_stats():
    """
    Get statistics about jobs in the vector database.
    
    Returns information about the number of jobs stored and collection statistics.
    
    **Returns:**
    - `collection_stats` (dict): Statistics from the vector database collection
    
    **Example:**
    ```bash
    GET /jobs/stats
    ```
    """
    try:
        from app.db.vector_store import get_collection_stats
        stats = get_collection_stats()
        return {
            "collection_stats": stats,
            "message": f"Vector database contains {stats.get('count', 0)} job embeddings"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving job stats: {str(e)}"
        )

