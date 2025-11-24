/**
 * Jobs API Service
 * 
 * Provides type-safe functions for job-related API calls
 */

import apiClient from './axios';
import type {
  ScrapeJobsRequest,
  ScrapeJobsResponse,
  MatchJobsResponse,
} from './types';

/**
 * Scrape job postings from public job boards and ingest them into the vector database
 * 
 * @param query - Job search query (e.g., "software engineer", "data scientist")
 * @param limit - Maximum number of jobs to scrape (default: 20, max: 100)
 * @returns Promise with scraping and ingestion summary
 */
export async function scrapeJobs(
  query: string,
  limit: number = 20
): Promise<ScrapeJobsResponse> {
  if (!query || query.trim() === '') {
    throw new Error('Query cannot be empty');
  }
  
  if (limit < 1 || limit > 100) {
    throw new Error('Limit must be between 1 and 100');
  }
  
  const request: ScrapeJobsRequest = {
    query: query.trim(),
    limit,
  };
  
  const response = await apiClient.post<ScrapeJobsResponse>(
    '/jobs/scrape',
    request
  );
  
  return response.data;
}

/**
 * Find jobs similar to the provided query text using semantic search
 * 
 * @param text - Query text describing the type of job (e.g., "backend developer", "Python engineer")
 * @param n - Number of similar jobs to return (default: 5, max: 20)
 * @returns Promise with list of matching jobs and similarity scores
 */
export async function matchJobs(
  text: string,
  n: number = 5
): Promise<MatchJobsResponse> {
  if (!text || text.trim() === '') {
    throw new Error('Query text cannot be empty');
  }
  
  if (n < 1 || n > 20) {
    throw new Error('Number of results must be between 1 and 20');
  }
  
  const response = await apiClient.get<MatchJobsResponse>(
    '/jobs/match',
    {
      params: {
        text: text.trim(),
        n,
      },
    }
  );
  
  return response.data;
}

