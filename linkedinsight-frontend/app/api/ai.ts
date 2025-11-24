/**
 * AI API Service
 * 
 * Provides type-safe functions for AI-powered API calls
 */

import apiClient from './axios';
import type {
  RoadmapRequest,
  RoadmapResponse,
  SkillGapsRequest,
  SkillGapsResponse,
} from './types';

/**
 * Generate a detailed 4-week learning roadmap for acquiring missing skills
 * 
 * @param skills - Array of skills the user needs to learn
 * @returns Promise with generated roadmap in Markdown format
 */
export async function generateRoadmap(
  skills: string[]
): Promise<RoadmapResponse> {
  if (!skills || skills.length === 0) {
    throw new Error('Skills array cannot be empty');
  }
  
  // Filter and validate skills
  const validSkills = skills
    .map(skill => skill.trim())
    .filter(skill => skill.length > 0);
  
  if (validSkills.length === 0) {
    throw new Error('No valid skills provided');
  }
  
  const request: RoadmapRequest = {
    missing_skills: validSkills,
  };
  
  const response = await apiClient.post<RoadmapResponse>(
    '/ai/roadmap',
    request
  );
  
  return response.data;
}

/**
 * Generate an AI explanation of skill gaps and their importance
 * 
 * @param userSkills - Array of skills the user currently has
 * @param missingSkills - Array of skills the user needs to acquire
 * @returns Promise with detailed explanation in Markdown format
 */
export async function explainSkillGaps(
  userSkills: string[],
  missingSkills: string[]
): Promise<SkillGapsResponse> {
  if (!missingSkills || missingSkills.length === 0) {
    throw new Error('Missing skills array cannot be empty');
  }
  
  // Filter and validate skills
  const validUserSkills = (userSkills || [])
    .map(skill => skill.trim())
    .filter(skill => skill.length > 0);
  
  const validMissingSkills = missingSkills
    .map(skill => skill.trim())
    .filter(skill => skill.length > 0);
  
  if (validMissingSkills.length === 0) {
    throw new Error('No valid missing skills provided');
  }
  
  const request: SkillGapsRequest = {
    user_skills: validUserSkills,
    missing_skills: validMissingSkills,
  };
  
  const response = await apiClient.post<SkillGapsResponse>(
    '/ai/explain-skill-gaps',
    request
  );
  
  return response.data;
}

