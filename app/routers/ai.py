"""
AI Router for LinkedInsight API.

This router provides AI-powered endpoints for:
- Generating personalized learning roadmaps
- Explaining skill gaps and their importance
- Providing career guidance and recommendations
"""

from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel, Field
from app.core.llm import generate_roadmap, explain_skill_gaps

router = APIRouter(prefix="/ai", tags=["ai"])


class RoadmapRequest(BaseModel):
    """Request model for generating learning roadmap."""
    missing_skills: List[str] = Field(
        ...,
        min_items=1,
        description="List of skills the user needs to learn"
    )


class RoadmapResponse(BaseModel):
    """Response model for learning roadmap."""
    skills: List[str]
    roadmap: str
    message: str


class SkillGapsRequest(BaseModel):
    """Request model for explaining skill gaps."""
    user_skills: List[str] = Field(
        ...,
        description="List of skills the user currently has"
    )
    missing_skills: List[str] = Field(
        ...,
        min_items=1,
        description="List of skills the user needs to acquire"
    )


class SkillGapsResponse(BaseModel):
    """Response model for skill gaps explanation."""
    user_skills: List[str]
    missing_skills: List[str]
    explanation: str
    message: str


@router.post("/roadmap", response_model=RoadmapResponse)
async def generate_learning_roadmap(request: RoadmapRequest):
    """
    Generate a detailed 4-week learning roadmap for acquiring missing skills.
    
    This endpoint uses AI to create a structured, actionable learning plan that helps
    users systematically acquire target skills. The roadmap includes weekly objectives,
    curated resources, and hands-on practice projects.
    
    **Request Body:**
    ```json
    {
        "missing_skills": ["Python", "Machine Learning", "Data Science"]
    }
    ```
    
    **Returns:**
    - `skills` (List[str]): The skills for which the roadmap was generated
    - `roadmap` (str): A detailed Markdown-formatted learning roadmap containing:
        - Overview and introduction
        - Week 1-4 breakdowns, each with:
            * Weekly objectives
            * Learning resources (courses, tutorials, documentation)
            * Practice projects
        - Summary and next steps
    - `message` (str): Human-readable summary
    
    **Example:**
    ```bash
    POST /ai/roadmap
    {
        "missing_skills": ["Python", "Machine Learning"]
    }
    ```
    
    **Response:**
    ```json
    {
        "skills": ["Python", "Machine Learning"],
        "roadmap": "# 4-Week Learning Roadmap: Python & Machine Learning\n\n...",
        "message": "Generated 4-week roadmap for 2 skills"
    }
    ```
    
    **Note:**
    The roadmap is generated using OpenAI's GPT models and may take a few seconds
    to generate. The content is personalized and actionable.
    """
    try:
        # Validate input
        if not request.missing_skills:
            raise HTTPException(status_code=400, detail="missing_skills list cannot be empty")
        
        # Filter and validate skills
        valid_skills = [skill.strip() for skill in request.missing_skills 
                       if skill and isinstance(skill, str) and skill.strip()]
        
        if not valid_skills:
            raise HTTPException(status_code=400, detail="No valid skills provided")
        
        # Generate roadmap using LLM
        print(f"Generating roadmap for skills: {valid_skills}")
        roadmap = generate_roadmap(valid_skills)
        
        return RoadmapResponse(
            skills=valid_skills,
            roadmap=roadmap,
            message=f"Generated 4-week roadmap for {len(valid_skills)} skill(s)"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating roadmap: {str(e)}"
        )


@router.post("/explain-skill-gaps", response_model=SkillGapsResponse)
async def explain_skill_gaps_endpoint(request: SkillGapsRequest):
    """
    Generate an AI explanation of skill gaps and their importance.
    
    This endpoint provides personalized insights about why missing skills are important,
    how they connect to the user's existing skills, and how they fit into broader career
    paths. This helps users understand the value of acquiring these skills and motivates
    them to learn.
    
    **Request Body:**
    ```json
    {
        "user_skills": ["Python", "SQL"],
        "missing_skills": ["Machine Learning", "Data Engineering"]
    }
    ```
    
    **Returns:**
    - `user_skills` (List[str]): The user's current skills
    - `missing_skills` (List[str]): The skills the user needs to acquire
    - `explanation` (str): A detailed Markdown-formatted explanation covering:
        - Overview of skill gaps and their significance
        - Why each missing skill matters in today's job market
        - How missing skills connect to and build upon existing skills
        - Career path implications and opportunities
        - Prioritization and learning approach recommendations
    - `message` (str): Human-readable summary
    
    **Example:**
    ```bash
    POST /ai/explain-skill-gaps
    {
        "user_skills": ["Python", "SQL"],
        "missing_skills": ["Machine Learning", "Data Engineering"]
    }
    ```
    
    **Response:**
    ```json
    {
        "user_skills": ["Python", "SQL"],
        "missing_skills": ["Machine Learning", "Data Engineering"],
        "explanation": "# Understanding Your Skill Gaps\n\n...",
        "message": "Generated explanation for 2 skill gaps based on 2 existing skills"
    }
    ```
    
    **Note:**
    The explanation is generated using OpenAI's GPT models and provides personalized,
    actionable insights tailored to the user's current skill set.
    """
    try:
        # Validate input
        if not request.missing_skills:
            raise HTTPException(status_code=400, detail="missing_skills list cannot be empty")
        
        # Filter and validate skills
        user_skills = [skill.strip() for skill in request.user_skills 
                      if skill and isinstance(skill, str) and skill.strip()]
        missing_skills = [skill.strip() for skill in request.missing_skills 
                         if skill and isinstance(skill, str) and skill.strip()]
        
        if not missing_skills:
            raise HTTPException(status_code=400, detail="No valid missing skills provided")
        
        # Generate explanation using LLM
        print(f"Generating skill gap explanation for {len(missing_skills)} missing skills")
        explanation = explain_skill_gaps(user_skills, missing_skills)
        
        return SkillGapsResponse(
            user_skills=user_skills,
            missing_skills=missing_skills,
            explanation=explanation,
            message=f"Generated explanation for {len(missing_skills)} skill gap(s) based on {len(user_skills)} existing skill(s)"
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating skill gap explanation: {str(e)}"
        )

