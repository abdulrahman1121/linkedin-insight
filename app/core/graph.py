"""
Skills Graph Engine for LinkedInsight using NetworkX.

This module implements a directed graph to model skill prerequisites and relationships.
The graph supports skill gap analysis by:
- Tracking prerequisite relationships between skills
- Generating learning paths to acquire target skills
- Identifying related skills for exploration and recommendations
- Supporting career navigation by showing skill dependencies

The graph is stored in module memory and persists for the application lifetime.
"""

import networkx as nx
from typing import List, Set, Optional
from collections import deque


# Initialize a directed graph to represent skill prerequisites
# Directed edges: prerequisite → skill (meaning you need prerequisite to learn skill)
# This graph persists in module memory throughout the application lifecycle
skills_graph = nx.DiGraph()


def add_skill(skill_name: str) -> bool:
    """
    Add a skill node to the skills graph if it doesn't already exist.
    
    This function ensures a skill is represented in the graph, which is necessary
    before creating relationships or querying prerequisites. If the skill already
    exists, the function returns True without modifying the graph.
    
    Args:
        skill_name (str): The name of the skill to add. Should be a non-empty string.
                         Skill names are case-sensitive.
    
    Returns:
        bool: True if the skill was added (or already exists), False if invalid input.
    
    Raises:
        ValueError: If skill_name is empty or not a string.
    
    Example:
        >>> add_skill("Python")
        True
        >>> add_skill("Machine Learning")
        True
    """
    if not skill_name or not isinstance(skill_name, str):
        raise ValueError("Skill name must be a non-empty string")
    
    skill_name = skill_name.strip()
    if not skill_name:
        raise ValueError("Skill name cannot be empty or whitespace only")
    
    # Add node if it doesn't exist (NetworkX handles duplicates gracefully)
    if not skills_graph.has_node(skill_name):
        skills_graph.add_node(skill_name)
    
    return True


def add_prerequisite(skill: str, prerequisite: str) -> bool:
    """
    Create a prerequisite relationship between two skills.
    
    This function establishes that 'prerequisite' must be learned before 'skill'.
    The relationship is represented as a directed edge: prerequisite → skill.
    Both skills are automatically added to the graph if they don't exist.
    
    This supports skill gap analysis by:
    - Identifying what skills a user needs to learn before a target skill
    - Building dependency chains for learning paths
    - Preventing circular dependencies (cycles)
    
    Args:
        skill (str): The target skill that requires the prerequisite.
        prerequisite (str): The skill that must be learned before the target skill.
    
    Returns:
        bool: True if the prerequisite relationship was successfully added.
    
    Raises:
        ValueError: If either skill name is invalid.
        ValueError: If adding the edge would create a cycle (circular dependency).
    
    Example:
        >>> add_prerequisite("Machine Learning", "Python")
        True
        >>> add_prerequisite("Deep Learning", "Machine Learning")
        True
        # This creates: Python → Machine Learning → Deep Learning
    """
    if not skill or not isinstance(skill, str):
        raise ValueError("Skill name must be a non-empty string")
    
    if not prerequisite or not isinstance(prerequisite, str):
        raise ValueError("Prerequisite name must be a non-empty string")
    
    skill = skill.strip()
    prerequisite = prerequisite.strip()
    
    if not skill or not prerequisite:
        raise ValueError("Skill and prerequisite names cannot be empty")
    
    if skill == prerequisite:
        raise ValueError("A skill cannot be a prerequisite of itself")
    
    # Ensure both nodes exist
    add_skill(skill)
    add_skill(prerequisite)
    
    # Check if adding this edge would create a cycle
    # We do this by temporarily adding the edge and checking for cycles
    if skills_graph.has_edge(prerequisite, skill):
        # Edge already exists, nothing to do
        return True
    
    # Check for cycles: if there's already a path from skill → prerequisite,
    # adding prerequisite → skill would create a cycle
    if nx.has_path(skills_graph, skill, prerequisite):
        raise ValueError(
            f"Adding prerequisite '{prerequisite}' → '{skill}' would create a circular dependency. "
            f"There is already a path from '{skill}' to '{prerequisite}'."
        )
    
    # Add the directed edge: prerequisite → skill
    skills_graph.add_edge(prerequisite, skill)
    
    return True


def get_prerequisites(skill: str) -> List[str]:
    """
    Get all direct prerequisites for a given skill.
    
    Returns only the immediate prerequisites (one step away in the graph).
    This is useful for understanding what skills are directly required before
    learning a target skill.
    
    Args:
        skill (str): The skill to query for prerequisites.
    
    Returns:
        List[str]: A list of skill names that are direct prerequisites.
                  Returns empty list if skill has no prerequisites or doesn't exist.
    
    Raises:
        ValueError: If skill name is invalid.
    
    Example:
        >>> add_prerequisite("Machine Learning", "Python")
        >>> add_prerequisite("Machine Learning", "Statistics")
        >>> get_prerequisites("Machine Learning")
        ['Python', 'Statistics']
    """
    if not skill or not isinstance(skill, str):
        raise ValueError("Skill name must be a non-empty string")
    
    skill = skill.strip()
    
    if not skills_graph.has_node(skill):
        return []
    
    # Get all predecessors (nodes with edges pointing to this skill)
    # In our graph, predecessors are prerequisites
    prerequisites = list(skills_graph.predecessors(skill))
    
    return sorted(prerequisites)  # Return sorted for consistency


def get_learning_path(target_skill: str) -> List[str]:
    """
    Generate an ordered learning path to acquire a target skill.
    
    This function uses topological sorting to determine the correct order
    in which prerequisites should be learned. The path includes all prerequisites
    in a valid learning order, ending with the target skill itself.
    
    The learning path supports skill gap analysis by:
    - Showing users exactly what skills they need to learn and in what order
    - Providing a roadmap from current skills to target skills
    - Identifying all transitive prerequisites (not just direct ones)
    
    Algorithm:
    - Uses topological sort to find a valid ordering
    - Includes all prerequisites reachable from the target skill
    - Ensures prerequisites are learned before skills that depend on them
    
    Args:
        target_skill (str): The skill for which to generate a learning path.
    
    Returns:
        List[str]: An ordered list of skills to learn, starting with foundational
                  skills and ending with the target skill. Returns empty list if
                  target skill doesn't exist or has no prerequisites.
    
    Raises:
        ValueError: If target skill name is invalid.
    
    Example:
        >>> add_prerequisite("Machine Learning", "Python")
        >>> add_prerequisite("Deep Learning", "Machine Learning")
        >>> get_learning_path("Deep Learning")
        ['Python', 'Machine Learning', 'Deep Learning']
    """
    if not target_skill or not isinstance(target_skill, str):
        raise ValueError("Target skill name must be a non-empty string")
    
    target_skill = target_skill.strip()
    
    if not skills_graph.has_node(target_skill):
        return []
    
    # Get all nodes that are reachable from the target skill (all prerequisites)
    # We need to reverse the graph to find all prerequisites
    # In the original graph: prerequisite → skill
    # In reversed graph: skill → prerequisite (easier to traverse backwards)
    reversed_graph = skills_graph.reverse()
    
    # Find all nodes reachable from target_skill in the reversed graph
    # These are all prerequisites (direct and transitive)
    if not nx.has_path(reversed_graph, target_skill, target_skill):
        # No prerequisites, return just the target skill
        return [target_skill]
    
    # Get all nodes in the subgraph containing target_skill and its prerequisites
    # We traverse backwards from target_skill to find all prerequisites
    reachable_nodes = set()
    
    # Use BFS to find all prerequisites
    queue = deque([target_skill])
    reachable_nodes.add(target_skill)
    
    while queue:
        current = queue.popleft()
        # In reversed graph, successors are prerequisites
        for predecessor in reversed_graph.successors(current):
            if predecessor not in reachable_nodes:
                reachable_nodes.add(predecessor)
                queue.append(predecessor)
    
    # Create subgraph with all relevant nodes
    subgraph = skills_graph.subgraph(reachable_nodes)
    
    # Perform topological sort to get valid learning order
    try:
        # Topological sort gives us a valid ordering
        learning_path = list(nx.topological_sort(subgraph))
    except nx.NetworkXError:
        # If there's a cycle (shouldn't happen due to our validation, but handle it)
        # Fall back to a simple DFS-based ordering
        learning_path = list(nx.dfs_tree(subgraph, target_skill).nodes())
        learning_path.reverse()
        # Ensure target_skill is at the end
        if target_skill in learning_path:
            learning_path.remove(target_skill)
        learning_path.append(target_skill)
    
    return learning_path


def get_related_skills(skill: str) -> dict:
    """
    Get all skills related to a given skill for exploration and recommendations.
    
    This function returns both prerequisites (what you need to know) and
    successors (what you can learn next). This supports skill gap analysis by:
    - Showing users what foundational skills they might be missing
    - Suggesting next steps after learning a skill
    - Enabling exploration of the skill ecosystem around a target skill
    
    Args:
        skill (str): The skill to query for related skills.
    
    Returns:
        dict: A dictionary with two keys:
            - 'prerequisites' (List[str]): Skills needed before this skill
            - 'successors' (List[str]): Skills that can be learned after this skill
            - 'all_related' (List[str]): Combined list of all related skills
    
    Raises:
        ValueError: If skill name is invalid.
    
    Example:
        >>> add_prerequisite("Machine Learning", "Python")
        >>> add_prerequisite("Deep Learning", "Machine Learning")
        >>> add_prerequisite("NLP", "Machine Learning")
        >>> get_related_skills("Machine Learning")
        {
            'prerequisites': ['Python'],
            'successors': ['Deep Learning', 'NLP'],
            'all_related': ['Python', 'Deep Learning', 'NLP']
        }
    """
    if not skill or not isinstance(skill, str):
        raise ValueError("Skill name must be a non-empty string")
    
    skill = skill.strip()
    
    if not skills_graph.has_node(skill):
        return {
            'prerequisites': [],
            'successors': [],
            'all_related': []
        }
    
    # Get prerequisites (predecessors in the graph)
    prerequisites = sorted(list(skills_graph.predecessors(skill)))
    
    # Get successors (skills that depend on this skill)
    successors = sorted(list(skills_graph.successors(skill)))
    
    # Combine all related skills
    all_related = sorted(list(set(prerequisites + successors)))
    
    return {
        'prerequisites': prerequisites,
        'successors': successors,
        'all_related': all_related
    }


def get_all_skills() -> List[str]:
    """
    Get a list of all skills currently in the graph.
    
    Returns:
        List[str]: A sorted list of all skill names in the graph.
    """
    return sorted(list(skills_graph.nodes()))


def get_graph_stats() -> dict:
    """
    Get statistics about the skills graph.
    
    Returns:
        dict: Dictionary containing:
            - 'num_skills' (int): Total number of skills (nodes)
            - 'num_relationships' (int): Total number of prerequisite relationships (edges)
            - 'is_dag' (bool): Whether the graph is a Directed Acyclic Graph (no cycles)
    """
    return {
        'num_skills': skills_graph.number_of_nodes(),
        'num_relationships': skills_graph.number_of_edges(),
        'is_dag': nx.is_directed_acyclic_graph(skills_graph)
    }

