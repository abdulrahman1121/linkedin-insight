/**
 * TypeScript Types and Interfaces for API Responses
 * 
 * Defines all response types for type-safe API calls
 */

// Health Check Response
export interface HealthResponse {
  status: string;
}

// System Test Response
export interface SystemTestResponse {
  db: string;
  graph: string;
  embeddings: string;
  vector_store: string;
}

// Skills API Types
export interface RelatedSkillsResponse {
  skill: string;
  prerequisites: string[];
  successors: string[];
  all_related: string[];
}

export interface PrerequisitesResponse {
  skill: string;
  prerequisites: string[];
  count: number;
}

export interface LearningPathResponse {
  target_skill: string;
  learning_path: string[];
  path_length: number;
  message: string;
}

// Jobs API Types
export interface ScrapeJobsRequest {
  query: string;
  limit: number;
}

export interface ScrapeJobsResponse {
  query: string;
  scraped_count: number;
  ingestion_summary: {
    total_jobs: number;
    processed: number;
    failed: number;
    errors: string[];
  };
  message: string;
}

export interface JobMatch {
  id: string;
  title: string;
  company: string;
  location: string;
  similarity: number;
  distance: number;
  url: string;
  programming_languages: string;
  technical_skills: string;
}

export interface MatchJobsResponse {
  query_text: string;
  matches: JobMatch[];
  count: number;
}

// AI API Types
export interface RoadmapRequest {
  missing_skills: string[];
}

export interface RoadmapResponse {
  skills: string[];
  roadmap: string;
  message: string;
}

export interface SkillGapsRequest {
  user_skills: string[];
  missing_skills: string[];
}

export interface SkillGapsResponse {
  user_skills: string[];
  missing_skills: string[];
  explanation: string;
  message: string;
}

