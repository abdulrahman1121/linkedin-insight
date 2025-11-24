"""
Skills Router for LinkedInsight API.

This router provides endpoints for querying the skills graph, including:
- Related skills (prerequisites and successors)
- Prerequisites for a skill
- Learning paths to acquire skills
"""

from fastapi import APIRouter, Query, HTTPException, Body
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from app.core.graph import (
    get_related_skills,
    get_prerequisites,
    get_learning_path,
    get_all_skills,
    get_graph_stats,
    add_skill,
    add_prerequisite
)

router = APIRouter(prefix="/skills", tags=["skills"])


def find_skill_case_insensitive(skill_name: str) -> str:
    """
    Find a skill in the graph using case-insensitive matching.
    
    Args:
        skill_name: The skill name to search for (case-insensitive)
    
    Returns:
        The exact skill name as stored in the graph, or the original name if not found
    """
    from app.core.graph import get_all_skills
    
    skill_name = skill_name.strip()
    all_skills = get_all_skills()
    
    # Try exact match first
    if skill_name in all_skills:
        return skill_name
    
    # Try case-insensitive match
    skill_lower = skill_name.lower()
    for skill in all_skills:
        if skill.lower() == skill_lower:
            return skill
    
    # If not found, return original (will be handled by graph functions)
    return skill_name


class RelatedSkillsResponse(BaseModel):
    """Response model for related skills endpoint."""
    skill: str
    prerequisites: List[str]
    successors: List[str]
    all_related: List[str]


class PrerequisitesResponse(BaseModel):
    """Response model for prerequisites endpoint."""
    skill: str
    prerequisites: List[str]
    count: int


class LearningPathResponse(BaseModel):
    """Response model for learning path endpoint."""
    target_skill: str
    learning_path: List[str]
    path_length: int
    message: str


@router.get("/graph/related", response_model=RelatedSkillsResponse)
def get_related_skills_endpoint(skill: str = Query(..., description="The skill to query for related skills")):
    """
    Get all skills related to a given skill.
    
    This endpoint returns prerequisites (skills needed before) and successors
    (skills that can be learned after) the specified skill. This helps users
    understand the skill ecosystem and plan their learning journey.
    
    **Query Parameters:**
    - `skill` (str): The skill name to query (e.g., "Python", "Machine Learning")
    
    **Returns:**
    - `skill` (str): The queried skill name
    - `prerequisites` (List[str]): Skills needed before this skill
    - `successors` (List[str]): Skills that can be learned after this skill
    - `all_related` (List[str]): Combined list of all related skills
    
    **Example:**
    ```bash
    GET /skills/graph/related?skill=Python
    ```
    
    **Response:**
    ```json
    {
        "skill": "Python",
        "prerequisites": [],
        "successors": ["Machine Learning", "Data Science"],
        "all_related": ["Machine Learning", "Data Science"]
    }
    ```
    """
    try:
        if not skill or not skill.strip():
            raise HTTPException(status_code=400, detail="Skill parameter cannot be empty")
        
        # Find skill with case-insensitive matching
        skill = find_skill_case_insensitive(skill)
        related = get_related_skills(skill)
        
        return RelatedSkillsResponse(
            skill=skill,
            prerequisites=related['prerequisites'],
            successors=related['successors'],
            all_related=related['all_related']
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving related skills: {str(e)}")


@router.get("/graph/prereqs", response_model=PrerequisitesResponse)
def get_prerequisites_endpoint(skill: str = Query(..., description="The skill to get prerequisites for")):
    """
    Get all direct prerequisites for a given skill.
    
    This endpoint returns only the immediate prerequisites (one step away in the graph)
    for the specified skill. This helps users understand what they need to learn
    directly before a target skill.
    
    **Query Parameters:**
    - `skill` (str): The skill name to query (e.g., "Machine Learning")
    
    **Returns:**
    - `skill` (str): The queried skill name
    - `prerequisites` (List[str]): Direct prerequisites for this skill
    - `count` (int): Number of prerequisites
    
    **Example:**
    ```bash
    GET /skills/graph/prereqs?skill=Machine Learning
    ```
    
    **Response:**
    ```json
    {
        "skill": "Machine Learning",
        "prerequisites": ["Python", "Statistics"],
        "count": 2
    }
    ```
    """
    try:
        if not skill or not skill.strip():
            raise HTTPException(status_code=400, detail="Skill parameter cannot be empty")
        
        # Find skill with case-insensitive matching
        skill = find_skill_case_insensitive(skill)
        prerequisites = get_prerequisites(skill)
        
        return PrerequisitesResponse(
            skill=skill,
            prerequisites=prerequisites,
            count=len(prerequisites)
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving prerequisites: {str(e)}")


@router.get("/graph/path", response_model=LearningPathResponse)
def get_learning_path_endpoint(skill: str = Query(..., description="The target skill to generate a learning path for")):
    """
    Generate an ordered learning path to acquire a target skill.
    
    This endpoint uses topological sorting to determine the correct order in which
    prerequisites should be learned. The path includes all prerequisites in a valid
    learning order, ending with the target skill itself.
    
    **Query Parameters:**
    - `skill` (str): The target skill to generate a learning path for
    
    **Returns:**
    - `target_skill` (str): The target skill name
    - `learning_path` (List[str]): Ordered list of skills to learn
    - `path_length` (int): Number of skills in the path
    - `message` (str): Human-readable description of the path
    
    **Example:**
    ```bash
    GET /skills/graph/path?skill=Deep Learning
    ```
    
    **Response:**
    ```json
    {
        "target_skill": "Deep Learning",
        "learning_path": ["Python", "Machine Learning", "Deep Learning"],
        "path_length": 3,
        "message": "Learn 3 skills in order: Python → Machine Learning → Deep Learning"
    }
    ```
    """
    try:
        if not skill or not skill.strip():
            raise HTTPException(status_code=400, detail="Skill parameter cannot be empty")
        
        # Find skill with case-insensitive matching
        skill = find_skill_case_insensitive(skill)
        path = get_learning_path(skill)
        
        if not path:
            return LearningPathResponse(
                target_skill=skill,
                learning_path=[],
                path_length=0,
                message=f"No learning path found for '{skill}'. The skill may not exist in the graph."
            )
        
        # Create a human-readable message
        if len(path) == 1:
            message = f"'{skill}' has no prerequisites. You can start learning it directly!"
        else:
            path_str = " → ".join(path)
            message = f"Learn {len(path)} skills in order: {path_str}"
        
        return LearningPathResponse(
            target_skill=skill,
            learning_path=path,
            path_length=len(path),
            message=message
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning path: {str(e)}")


@router.get("/all")
def get_all_skills_endpoint():
    """
    Get a list of all skills currently in the skills graph.
    
    This endpoint returns all skills that have been added to the graph,
    useful for exploration and discovery.
    
    **Returns:**
    - `skills` (List[str]): Sorted list of all skill names
    - `count` (int): Total number of skills
    
    **Example:**
    ```bash
    GET /skills/all
    ```
    """
    try:
        skills = get_all_skills()
        return {
            "skills": skills,
            "count": len(skills)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving skills: {str(e)}")


@router.get("/graph/stats")
def get_graph_stats_endpoint():
    """
    Get statistics about the skills graph.
    
    Returns information about the graph structure including number of skills,
    relationships, and whether it's a valid DAG (Directed Acyclic Graph).
    
    **Returns:**
    - `num_skills` (int): Total number of skills (nodes)
    - `num_relationships` (int): Total number of prerequisite relationships (edges)
    - `is_dag` (bool): Whether the graph is acyclic (no circular dependencies)
    
    **Example:**
    ```bash
    GET /skills/graph/stats
    ```
    """
    try:
        stats = get_graph_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving graph stats: {str(e)}")


class AddSkillRequest(BaseModel):
    """Request model for adding a skill."""
    skill: str = Field(..., description="The skill name to add")


class AddPrerequisiteRequest(BaseModel):
    """Request model for adding a prerequisite relationship."""
    skill: str = Field(..., description="The skill that requires the prerequisite")
    prerequisite: str = Field(..., description="The prerequisite skill")


@router.post("/add")
def add_skill_endpoint(request: AddSkillRequest = Body(...)):
    """
    Add a skill to the skills graph.
    
    This endpoint allows you to add a new skill node to the graph.
    The skill will be available for creating relationships and querying.
    
    **Request Body:**
    - `skill` (str): The skill name to add
    
    **Returns:**
    - `success` (bool): Whether the skill was added successfully
    - `skill` (str): The skill name that was added
    - `message` (str): Status message
    
    **Example:**
    ```bash
    POST /skills/add
    {
        "skill": "Python"
    }
    ```
    """
    try:
        if not request.skill or not request.skill.strip():
            raise HTTPException(status_code=400, detail="Skill name cannot be empty")
        
        skill = request.skill.strip()
        add_skill(skill)
        
        return {
            "success": True,
            "skill": skill,
            "message": f"Skill '{skill}' added successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding skill: {str(e)}")


@router.post("/add-prerequisite")
def add_prerequisite_endpoint(request: AddPrerequisiteRequest = Body(...)):
    """
    Add a prerequisite relationship between two skills.
    
    This endpoint creates a directed edge in the graph: prerequisite → skill.
    This means the prerequisite must be learned before the skill.
    
    **Request Body:**
    - `skill` (str): The skill that requires the prerequisite
    - `prerequisite` (str): The prerequisite skill
    
    **Returns:**
    - `success` (bool): Whether the relationship was added successfully
    - `skill` (str): The skill name
    - `prerequisite` (str): The prerequisite name
    - `message` (str): Status message
    
    **Example:**
    ```bash
    POST /skills/add-prerequisite
    {
        "skill": "Machine Learning",
        "prerequisite": "Python"
    }
    ```
    """
    try:
        if not request.skill or not request.skill.strip():
            raise HTTPException(status_code=400, detail="Skill name cannot be empty")
        if not request.prerequisite or not request.prerequisite.strip():
            raise HTTPException(status_code=400, detail="Prerequisite name cannot be empty")
        
        skill = request.skill.strip()
        prerequisite = request.prerequisite.strip()
        
        add_prerequisite(skill, prerequisite)
        
        return {
            "success": True,
            "skill": skill,
            "prerequisite": prerequisite,
            "message": f"Prerequisite relationship added: '{prerequisite}' → '{skill}'"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding prerequisite: {str(e)}")

