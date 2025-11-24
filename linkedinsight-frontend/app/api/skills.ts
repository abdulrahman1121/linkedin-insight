/**
 * Skills API Service
 * 
 * Provides type-safe functions for skills graph API calls
 */

import apiClient from './axios';
import type {
  RelatedSkillsResponse,
  PrerequisitesResponse,
  LearningPathResponse,
} from './types';

export interface AllSkillsResponse {
  skills: string[];
  count: number;
}

/**
 * Get all available skills in the graph
 * 
 * @returns Promise with list of all skills and count
 */
export async function getAllSkills(): Promise<AllSkillsResponse> {
  const response = await apiClient.get<AllSkillsResponse>('/skills/all');
  return response.data;
}

/**
 * Get all skills related to a given skill (prerequisites and successors)
 * 
 * @param skill - The skill name to query (e.g., "Python", "Machine Learning")
 * @returns Promise with related skills including prerequisites and successors
 */
export async function getRelated(skill: string): Promise<RelatedSkillsResponse> {
  if (!skill || skill.trim() === '') {
    throw new Error('Skill name cannot be empty');
  }
  
  const response = await apiClient.get<RelatedSkillsResponse>(
    '/skills/graph/related',
    {
      params: {
        skill: skill.trim(),
      },
    }
  );
  
  return response.data;
}

/**
 * Get all direct prerequisites for a given skill
 * 
 * @param skill - The skill name to query (e.g., "Machine Learning")
 * @returns Promise with list of prerequisites and count
 */
export async function getPrereqs(skill: string): Promise<PrerequisitesResponse> {
  if (!skill || skill.trim() === '') {
    throw new Error('Skill name cannot be empty');
  }
  
  const response = await apiClient.get<PrerequisitesResponse>(
    '/skills/graph/prereqs',
    {
      params: {
        skill: skill.trim(),
      },
    }
  );
  
  return response.data;
}

/**
 * Generate an ordered learning path to acquire a target skill
 * 
 * @param skill - The target skill to generate a learning path for
 * @returns Promise with ordered learning path and metadata
 */
export async function getLearningPath(skill: string): Promise<LearningPathResponse> {
  if (!skill || skill.trim() === '') {
    throw new Error('Skill name cannot be empty');
  }
  
  const response = await apiClient.get<LearningPathResponse>(
    '/skills/graph/path',
    {
      params: {
        skill: skill.trim(),
      },
    }
  );
  
  return response.data;
}

