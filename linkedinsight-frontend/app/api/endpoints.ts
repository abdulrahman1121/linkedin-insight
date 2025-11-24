/**
 * API Endpoints
 * 
 * Type-safe API endpoint definitions for the LinkedInsight backend.
 */

import { apiClient } from './client';

// Health check
export const healthCheck = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

// System test
export const systemTest = async () => {
  const response = await apiClient.get('/test/system');
  return response.data;
};

// Skills endpoints
export const getRelatedSkills = async (skill: string) => {
  const response = await apiClient.get(`/skills/graph/related?skill=${encodeURIComponent(skill)}`);
  return response.data;
};

export const getPrerequisites = async (skill: string) => {
  const response = await apiClient.get(`/skills/graph/prereqs?skill=${encodeURIComponent(skill)}`);
  return response.data;
};

export const getLearningPath = async (skill: string) => {
  const response = await apiClient.get(`/skills/graph/path?skill=${encodeURIComponent(skill)}`);
  return response.data;
};

// Jobs endpoints
export const scrapeJobs = async (query: string, limit: number = 20) => {
  const response = await apiClient.post('/jobs/scrape', { query, limit });
  return response.data;
};

export const matchJobs = async (text: string, n: number = 5) => {
  const response = await apiClient.get(`/jobs/match?text=${encodeURIComponent(text)}&n=${n}`);
  return response.data;
};

// AI endpoints
export const generateRoadmap = async (missingSkills: string[]) => {
  const response = await apiClient.post('/ai/roadmap', { missing_skills: missingSkills });
  return response.data;
};

export const explainSkillGaps = async (userSkills: string[], missingSkills: string[]) => {
  const response = await apiClient.post('/ai/explain-skill-gaps', {
    user_skills: userSkills,
    missing_skills: missingSkills,
  });
  return response.data;
};

