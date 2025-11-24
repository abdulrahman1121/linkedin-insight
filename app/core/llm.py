"""
LLM Reasoning Engine for LinkedInsight.

This module provides AI-powered reasoning capabilities using OpenAI's GPT models.
It generates personalized learning roadmaps and explains skill gaps to help users
navigate their career development journey.

The module supports:
- Generating structured learning roadmaps for skill acquisition
- Explaining skill gaps and their importance in career development
- Connecting user's current skills to missing skills
- Providing actionable insights for career growth
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import List, Optional

# Load environment variables
load_dotenv()

# Initialize OpenAI client with timeout
# Uses the same API key as the embeddings service
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=30.0  # 30 second timeout for all requests
)

# Default model for chat completions
# Using GPT-4 for better reasoning capabilities, with fallback to GPT-3.5-turbo
DEFAULT_MODEL = "gpt-4o-mini"  # Cost-effective with good reasoning
FALLBACK_MODEL = "gpt-3.5-turbo"


def generate_roadmap(skills: List[str], model: Optional[str] = None) -> str:
    """
    Generate a detailed 4-week learning roadmap for acquiring missing skills.
    
    This function uses OpenAI's chat completions API to create a structured,
    actionable learning plan. The roadmap is designed to help users systematically
    acquire the target skills through weekly objectives, curated resources, and
    hands-on practice projects.
    
    The generated roadmap includes:
    - Week-by-week breakdown with clear objectives
    - Recommended learning resources (courses, tutorials, documentation)
    - Practice projects that reinforce learning
    - Progressive difficulty from foundational to advanced concepts
    
    Args:
        skills (List[str]): A list of skills the user needs to learn.
                          Should not be empty. Each skill should be clearly named.
        model (Optional[str]): The OpenAI model to use. Defaults to DEFAULT_MODEL.
                              Can be overridden for different quality/cost trade-offs.
    
    Returns:
        str: A formatted learning roadmap as Markdown text. The roadmap includes:
            - Introduction and overview
            - 4 weekly sections, each with:
              * Weekly objectives
              * Learning resources
              * Practice project
            - Summary and next steps
    
    Raises:
        ValueError: If skills list is empty or contains invalid entries.
        Exception: If OpenAI API call fails (network error, API error, etc.).
    
    Example:
        >>> roadmap = generate_roadmap(["Python", "Machine Learning"])
        >>> print(roadmap)
        # 4-Week Learning Roadmap: Python & Machine Learning
        ...
    """
    if not skills or not isinstance(skills, list):
        raise ValueError("Skills must be a non-empty list")
    
    if len(skills) == 0:
        raise ValueError("Skills list cannot be empty")
    
    # Filter out empty or invalid skills
    valid_skills = [skill.strip() for skill in skills if skill and isinstance(skill, str) and skill.strip()]
    
    if len(valid_skills) == 0:
        raise ValueError("No valid skills provided in the list")
    
    # Use provided model or default
    model_to_use = model or DEFAULT_MODEL
    
    # Construct the prompt for the LLM
    skills_str = ", ".join(valid_skills)
    
    system_prompt = """You are an expert career coach creating concise, actionable learning roadmaps."""
    
    user_prompt = f"""Create a 4-week learning roadmap for: {skills_str}

Format as Markdown with:
1. **Overview** (2-3 sentences)
2. **Week 1-4** (each with: Objectives, Resources, Project - keep brief)
3. **Next Steps** (2-3 sentences)

Be concise and practical. Include specific resource names."""
    
    try:
        # Call OpenAI API with optimized settings for speed
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,  # Slightly lower for faster, more consistent responses
            max_tokens=1200  # Reduced for faster generation while still comprehensive
        )
        
        # Extract the generated roadmap
        roadmap = response.choices[0].message.content.strip()
        
        return roadmap
    
    except Exception as e:
        # Provide helpful error messages
        error_msg = f"Failed to generate roadmap: {str(e)}"
        print(error_msg)
        raise Exception(error_msg) from e


def explain_skill_gaps(
    user_skills: List[str], 
    missing_skills: List[str],
    model: Optional[str] = None
) -> str:
    """
    Generate an AI explanation of skill gaps and their importance.
    
    This function provides personalized insights about why missing skills are important,
    how they connect to the user's existing skills, and how they fit into broader
    career paths. This helps users understand the value of acquiring these skills
    and motivates them to learn.
    
    The explanation covers:
    - Why each missing skill is important for career growth
    - How missing skills connect to and build upon existing skills
    - Career paths and opportunities these skills unlock
    - Practical benefits of acquiring these skills
    
    Args:
        user_skills (List[str]): List of skills the user currently possesses.
                                Used to show connections and build context.
        missing_skills (List[str]): List of skills the user needs to acquire.
                                   These are the focus of the explanation.
        model (Optional[str]): The OpenAI model to use. Defaults to DEFAULT_MODEL.
    
    Returns:
        str: A formatted explanation as Markdown text. The explanation includes:
            - Overview of skill gaps
            - Importance of each missing skill
            - Connections to existing skills
            - Career path implications
            - Actionable insights
    
    Raises:
        ValueError: If either list is empty or contains invalid entries.
        Exception: If OpenAI API call fails.
    
    Example:
        >>> explanation = explain_skill_gaps(
        ...     ["Python", "SQL"],
        ...     ["Machine Learning", "Data Engineering"]
        ... )
        >>> print(explanation)
        # Understanding Your Skill Gaps
        ...
    """
    if not isinstance(user_skills, list):
        raise ValueError("user_skills must be a list")
    
    if not isinstance(missing_skills, list):
        raise ValueError("missing_skills must be a list")
    
    # Filter and validate skills
    valid_user_skills = [skill.strip() for skill in user_skills 
                        if skill and isinstance(skill, str) and skill.strip()]
    valid_missing_skills = [skill.strip() for skill in missing_skills 
                           if skill and isinstance(skill, str) and skill.strip()]
    
    if len(valid_missing_skills) == 0:
        raise ValueError("missing_skills list cannot be empty")
    
    # Use provided model or default
    model_to_use = model or DEFAULT_MODEL
    
    # Construct the prompt
    user_skills_str = ", ".join(valid_user_skills) if valid_user_skills else "None specified"
    missing_skills_str = ", ".join(valid_missing_skills)
    
    system_prompt = """You are an expert career advisor. Provide clear, concise skill gap explanations."""
    
    user_prompt = f"""Current Skills: {user_skills_str}
Missing Skills: {missing_skills_str}

Explain in Markdown:
1. **Overview** (2-3 sentences)
2. **Why Each Skill Matters** (brief for each)
3. **Connections** (how missing skills build on current ones)
4. **Career Impact** (what opportunities open up)
5. **Next Steps** (prioritization and approach)

Be concise and actionable."""
    
    try:
        # Call OpenAI API with optimized settings for speed
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.6,  # Slightly lower for faster responses
            max_tokens=1200  # Reduced for faster generation
        )
        
        # Extract the generated explanation
        explanation = response.choices[0].message.content.strip()
        
        return explanation
    
    except Exception as e:
        # Provide helpful error messages
        error_msg = f"Failed to generate skill gap explanation: {str(e)}"
        print(error_msg)
        raise Exception(error_msg) from e


def generate_skill_recommendations(
    user_skills: List[str],
    target_role: Optional[str] = None,
    model: Optional[str] = None
) -> str:
    """
    Generate AI-powered skill recommendations based on current skills and career goals.
    
    This function suggests skills that would be valuable to learn next, either
    based on the user's current skill set or aligned with a target role.
    
    Args:
        user_skills (List[str]): List of skills the user currently has.
        target_role (Optional[str]): Target job role or career path. If provided,
                                    recommendations will be aligned with this role.
        model (Optional[str]): The OpenAI model to use. Defaults to DEFAULT_MODEL.
    
    Returns:
        str: A formatted recommendation as Markdown text with suggested skills
            and explanations of why they're valuable.
    
    Raises:
        ValueError: If user_skills is empty or invalid.
        Exception: If OpenAI API call fails.
    """
    if not isinstance(user_skills, list) or len(user_skills) == 0:
        raise ValueError("user_skills must be a non-empty list")
    
    # Filter and validate skills
    valid_user_skills = [skill.strip() for skill in user_skills 
                        if skill and isinstance(skill, str) and skill.strip()]
    
    if len(valid_user_skills) == 0:
        raise ValueError("No valid skills provided")
    
    model_to_use = model or DEFAULT_MODEL
    
    user_skills_str = ", ".join(valid_user_skills)
    role_context = f" for a {target_role}" if target_role else ""
    
    system_prompt = """You are an expert career advisor specializing in technical skill 
development. You provide insightful recommendations for skill acquisition."""
    
    user_prompt = f"""Based on the following current skills: {user_skills_str}

Recommend 5-7 skills that would be valuable to learn next{role_context}.

For each recommended skill, provide:
- Why it's a good next step
- How it connects to existing skills
- What it enables the user to do
- Suggested learning approach

Format as clean Markdown."""
    
    try:
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        error_msg = f"Failed to generate skill recommendations: {str(e)}"
        print(error_msg)
        raise Exception(error_msg) from e

