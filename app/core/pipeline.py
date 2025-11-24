"""
Job Data Ingestion Pipeline for LinkedInsight.

This module implements a complete pipeline for scraping, processing, and ingesting
job postings into the vector database. The pipeline consists of three main stages:

1. **Scraping**: Extracts job postings from publicly accessible job boards
2. **NLP Extraction**: Uses spaCy to extract skills and requirements from descriptions
3. **Vector DB Ingestion**: Stores processed jobs with embeddings for semantic search

The pipeline enables LinkedInsight to:
- Continuously update its job database
- Extract structured information from unstructured job descriptions
- Enable semantic search for job matching
"""

import requests
from bs4 import BeautifulSoup
import spacy
import re
from typing import List, Dict, Any, Optional
from urllib.parse import quote, urljoin
import time
import hashlib
from app.db.vector_store import add_job_embedding


# Load spaCy English model for NLP processing
# This model is used for named entity recognition and text processing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback: if model not loaded, we'll use regex-based extraction
    nlp = None
    print("Warning: spaCy model 'en_core_web_sm' not found. Using regex-based extraction.")


# Common programming languages and technical skills for extraction
PROGRAMMING_LANGUAGES = {
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'go', 'rust',
    'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
    'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express'
}

TECHNICAL_SKILLS = {
    'machine learning', 'deep learning', 'ai', 'artificial intelligence',
    'data science', 'data analysis', 'big data', 'cloud computing', 'aws', 'azure', 'gcp',
    'docker', 'kubernetes', 'devops', 'ci/cd', 'agile', 'scrum', 'git', 'linux',
    'database', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis'
}


def scrape_job_postings(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Scrape publicly available job listings from job boards.
    
    This function searches for job postings on publicly accessible job boards
    (like Indeed's public search results) and extracts structured information.
    The scraping is done respectfully with rate limiting and proper headers.
    
    **Scraping Stage:**
    - Constructs search URLs for job boards
    - Sends HTTP requests with proper headers
    - Parses HTML using BeautifulSoup
    - Extracts job title, company, location, and description
    - Returns structured job data
    
    Args:
        query (str): Job search query (e.g., "software engineer", "data scientist").
                    Will be URL-encoded for the search.
        limit (int, optional): Maximum number of jobs to scrape. Defaults to 20.
                              Should be reasonable to avoid overloading servers.
    
    Returns:
        List[Dict[str, Any]]: A list of job dictionaries, each containing:
            - title (str): Job title
            - company (str): Company name
            - location (str): Job location
            - description (str): Full job description text
            - url (str): URL of the job posting (if available)
            - source (str): Source of the job posting
    
    Raises:
        ValueError: If query is empty or limit is invalid.
        Exception: If scraping fails (network error, parsing error, etc.).
    
    Example:
        >>> jobs = scrape_job_postings("Python developer", limit=10)
        >>> print(f"Scraped {len(jobs)} jobs")
        Scraped 10 jobs
    """
    if not query or not isinstance(query, str) or not query.strip():
        raise ValueError("Query must be a non-empty string")
    
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit must be a positive integer")
    
    query = query.strip()
    jobs = []
    
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        # Scrape from Indeed (public search results)
        # Indeed's public search URL format
        encoded_query = quote(query)
        indeed_url = f"https://www.indeed.com/jobs?q={encoded_query}&l="
        
        print(f"Scraping jobs for query: '{query}' from Indeed...")
        
        # Send request with rate limiting
        response = requests.get(indeed_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job postings - Indeed uses specific class names
        # Note: These selectors may need adjustment if Indeed changes their HTML structure
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        if not job_cards:
            # Try alternative selector
            job_cards = soup.find_all('a', {'data-jk': True})
        
        jobs_scraped = 0
        
        for card in job_cards[:limit]:
            try:
                job_data = {}
                
                # Extract job title
                title_elem = card.find('h2', class_='jobTitle') or card.find('a', class_='jcs-JobTitle')
                if title_elem:
                    job_data['title'] = title_elem.get_text(strip=True)
                else:
                    # Fallback: try to find any h2 or title element
                    title_elem = card.find('h2') or card.find('a')
                    job_data['title'] = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                # Extract company name
                company_elem = card.find('span', class_='companyName') or card.find('a', class_='companyName')
                if company_elem:
                    job_data['company'] = company_elem.get_text(strip=True)
                else:
                    company_elem = card.find('span', {'data-testid': 'company-name'})
                    job_data['company'] = company_elem.get_text(strip=True) if company_elem else "N/A"
                
                # Extract location
                location_elem = card.find('div', class_='companyLocation') or card.find('div', {'data-testid': 'text-location'})
                if location_elem:
                    job_data['location'] = location_elem.get_text(strip=True)
                else:
                    job_data['location'] = "N/A"
                
                # Extract job URL
                link_elem = card.find('a', href=True)
                if link_elem:
                    href = link_elem.get('href', '')
                    if href.startswith('/'):
                        job_data['url'] = urljoin('https://www.indeed.com', href)
                    else:
                        job_data['url'] = href
                else:
                    job_data['url'] = ""
                
                # For full description, we'd need to visit each job page
                # For now, extract snippet if available
                snippet_elem = card.find('div', class_='job-snippet') or card.find('span', class_='job-snippet')
                if snippet_elem:
                    job_data['description'] = snippet_elem.get_text(strip=True)
                else:
                    job_data['description'] = ""
                
                job_data['source'] = 'indeed'
                
                # Only add if we have at least a title
                if job_data.get('title') and job_data['title'] != "N/A":
                    jobs.append(job_data)
                    jobs_scraped += 1
                
                # Rate limiting: small delay between requests
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error parsing job card: {str(e)}")
                continue
        
        print(f"Successfully scraped {len(jobs)} jobs")
        return jobs
    
    except requests.RequestException as e:
        error_msg = f"Network error while scraping jobs: {str(e)}"
        print(error_msg)
        raise Exception(error_msg) from e
    except Exception as e:
        error_msg = f"Error scraping job postings: {str(e)}"
        print(error_msg)
        raise Exception(error_msg) from e


def extract_skills_from_description(description: str) -> Dict[str, Any]:
    """
    Extract skills, programming languages, and requirements from job description.
    
    This function uses NLP (spaCy) and pattern matching to extract structured
    information from unstructured job descriptions. It identifies:
    - Required skills
    - Preferred skills
    - Programming languages
    - Technical skills
    
    **NLP Extraction Stage:**
    - Uses spaCy for named entity recognition and text processing
    - Applies pattern matching for known technical terms
    - Normalizes extracted skills (lowercase, strip whitespace)
    - Categorizes skills into required vs preferred based on context
    
    Args:
        description (str): The job description text to analyze.
                          Should be the full description for best results.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - required_skills (List[str]): Skills marked as required
            - preferred_skills (List[str]): Skills marked as preferred/nice-to-have
            - programming_languages (List[str]): Programming languages mentioned
            - technical_skills (List[str]): Technical skills and tools
            - all_skills (List[str]): Combined list of all extracted skills
    
    Example:
        >>> desc = "Looking for Python developer with 3+ years experience. 
        ...         Knowledge of Django and PostgreSQL preferred."
        >>> skills = extract_skills_from_description(desc)
        >>> print(skills['programming_languages'])
        ['python']
    """
    if not description or not isinstance(description, str):
        return {
            'required_skills': [],
            'preferred_skills': [],
            'programming_languages': [],
            'technical_skills': [],
            'all_skills': []
        }
    
    description = description.strip()
    if not description:
        return {
            'required_skills': [],
            'preferred_skills': [],
            'programming_languages': [],
            'technical_skills': [],
            'all_skills': []
        }
    
    # Normalize text to lowercase for matching
    desc_lower = description.lower()
    
    # Initialize result dictionaries
    required_skills = []
    preferred_skills = []
    programming_languages = []
    technical_skills = []
    
    # Extract programming languages
    for lang in PROGRAMMING_LANGUAGES:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(lang.lower()) + r'\b'
        if re.search(pattern, desc_lower):
            normalized_lang = lang.lower().strip()
            if normalized_lang not in programming_languages:
                programming_languages.append(normalized_lang)
    
    # Extract technical skills
    for skill in TECHNICAL_SKILLS:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, desc_lower):
            normalized_skill = skill.lower().strip()
            if normalized_skill not in technical_skills:
                technical_skills.append(normalized_skill)
    
    # Use spaCy for more advanced extraction if available
    if nlp:
        try:
            doc = nlp(description)
            
            # Extract noun phrases that might be skills
            # Look for patterns like "X experience", "knowledge of X", "familiarity with X"
            skill_patterns = [
                r'(?:experience|knowledge|familiarity|proficiency|expertise)\s+(?:with|in|of)\s+(\w+(?:\s+\w+)?)',
                r'(\w+(?:\s+\w+)?)\s+(?:experience|knowledge|skills)',
            ]
            
            for pattern in skill_patterns:
                matches = re.finditer(pattern, description, re.IGNORECASE)
                for match in matches:
                    skill = match.group(1).lower().strip()
                    if len(skill) > 2 and skill not in programming_languages and skill not in technical_skills:
                        # Determine if required or preferred based on context
                        context = match.group(0).lower()
                        if any(word in context for word in ['required', 'must', 'need', 'essential']):
                            if skill not in required_skills:
                                required_skills.append(skill)
                        elif any(word in context for word in ['preferred', 'nice', 'bonus', 'plus']):
                            if skill not in preferred_skills:
                                preferred_skills.append(skill)
                        else:
                            # Default to required if unclear
                            if skill not in required_skills:
                                required_skills.append(skill)
        except Exception as e:
            print(f"Error in spaCy processing: {str(e)}")
    
    # Fallback: simple keyword extraction if spaCy not available
    if not nlp:
        # Look for common skill indicators
        skill_indicators = ['experience with', 'knowledge of', 'proficient in', 'familiar with']
        for indicator in skill_indicators:
            pattern = rf'{indicator}\s+([a-zA-Z\s]+?)(?:\.|,|;|$)'
            matches = re.finditer(pattern, description, re.IGNORECASE)
            for match in matches:
                skill = match.group(1).lower().strip()
                if len(skill) > 2 and skill not in programming_languages and skill not in technical_skills:
                    if skill not in required_skills:
                        required_skills.append(skill)
    
    # Combine all skills
    all_skills = list(set(programming_languages + technical_skills + required_skills + preferred_skills))
    
    return {
        'required_skills': sorted(list(set(required_skills))),
        'preferred_skills': sorted(list(set(preferred_skills))),
        'programming_languages': sorted(programming_languages),
        'technical_skills': sorted(technical_skills),
        'all_skills': sorted(all_skills)
    }


def ingest_jobs_into_vector_db(jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ingest processed job postings into the vector database.
    
    This function takes scraped and processed job postings and stores them
    in the vector database with embeddings. Each job is:
    - Combined into a single text for embedding (title + description)
    - Embedded using OpenAI's embedding model
    - Stored in ChromaDB with rich metadata
    
    **Vector DB Ingestion Stage:**
    - Combines job title and description into embedding text
    - Generates embeddings using the embeddings service
    - Stores in vector database with metadata for filtering
    - Creates unique IDs for each job posting
    - Handles errors gracefully to continue processing other jobs
    
    Args:
        jobs (List[Dict[str, Any]]): List of job dictionaries from scraping.
                                    Each job should have at least 'title' and 'description'.
                                    Can include 'company', 'location', 'url', 'skills', etc.
    
    Returns:
        Dict[str, Any]: Summary dictionary containing:
            - total_jobs (int): Total number of jobs in input
            - processed (int): Number of jobs successfully processed
            - failed (int): Number of jobs that failed to process
            - errors (List[str]): List of error messages for failed jobs
    
    Raises:
        ValueError: If jobs is not a list or is empty.
    
    Example:
        >>> jobs = scrape_job_postings("Python developer", limit=5)
        >>> result = ingest_jobs_into_vector_db(jobs)
        >>> print(f"Processed {result['processed']} jobs")
        Processed 5 jobs
    """
    if not isinstance(jobs, list):
        raise ValueError("Jobs must be a list")
    
    if len(jobs) == 0:
        return {
            'total_jobs': 0,
            'processed': 0,
            'failed': 0,
            'errors': []
        }
    
    processed = 0
    failed = 0
    errors = []
    
    print(f"Starting ingestion of {len(jobs)} jobs into vector database...")
    
    for i, job in enumerate(jobs):
        try:
            # Validate required fields
            if not job.get('title'):
                errors.append(f"Job {i+1}: Missing title")
                failed += 1
                continue
            
            title = job.get('title', '').strip()
            description = job.get('description', '').strip()
            
            if not description:
                # If no description, use title only
                embedding_text = title
            else:
                # Combine title and description for embedding
                # This gives better semantic representation
                embedding_text = f"{title}\n\n{description}"
            
            # Generate unique ID for the job
            # Use hash of title + company + location for uniqueness
            job_id_str = f"{title}_{job.get('company', '')}_{job.get('location', '')}"
            job_id = hashlib.md5(job_id_str.encode()).hexdigest()
            
            # Extract skills if not already extracted
            if 'skills' not in job:
                skills_data = extract_skills_from_description(description)
                job['skills'] = skills_data
            
            # Prepare metadata for vector store
            metadata = {
                'title': title,
                'company': job.get('company', 'N/A'),
                'location': job.get('location', 'N/A'),
                'url': job.get('url', ''),
                'source': job.get('source', 'unknown'),
                'programming_languages': ', '.join(job['skills'].get('programming_languages', [])),
                'technical_skills': ', '.join(job['skills'].get('technical_skills', [])),
                'required_skills': ', '.join(job['skills'].get('required_skills', [])),
            }
            
            # Add to vector database
            success = add_job_embedding(
                id=job_id,
                text=embedding_text,
                metadata=metadata
            )
            
            if success:
                processed += 1
                if (i + 1) % 5 == 0:
                    print(f"Processed {i + 1}/{len(jobs)} jobs...")
            else:
                failed += 1
                errors.append(f"Job {i+1} ({title}): Failed to add to vector store")
        
        except Exception as e:
            failed += 1
            error_msg = f"Job {i+1}: {str(e)}"
            errors.append(error_msg)
            print(f"Error processing job {i+1}: {str(e)}")
            continue
    
    print(f"Ingestion complete: {processed} processed, {failed} failed")
    
    return {
        'total_jobs': len(jobs),
        'processed': processed,
        'failed': failed,
        'errors': errors
    }


def run_full_pipeline(query: str, limit: int = 20) -> Dict[str, Any]:
    """
    Run the complete job ingestion pipeline from start to finish.
    
    This is a convenience function that orchestrates all three stages:
    1. Scraping job postings
    2. Extracting skills from descriptions
    3. Ingesting into vector database
    
    Args:
        query (str): Job search query
        limit (int): Maximum number of jobs to process
    
    Returns:
        Dict[str, Any]: Combined results from all pipeline stages
    """
    print(f"Starting full pipeline for query: '{query}'")
    
    # Stage 1: Scraping
    jobs = scrape_job_postings(query, limit)
    
    # Stage 2: Extract skills for each job
    for job in jobs:
        if job.get('description'):
            job['skills'] = extract_skills_from_description(job['description'])
    
    # Stage 3: Ingest into vector database
    ingestion_result = ingest_jobs_into_vector_db(jobs)
    
    return {
        'scraped': len(jobs),
        'ingestion': ingestion_result
    }

