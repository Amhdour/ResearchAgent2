"""
Planner Agent - Task Decomposition and Orchestration

Role: Cognition Layer
Responsibility: Breaks down complex research queries into manageable subtasks

Educational Concept:
The Planner Agent demonstrates 'hierarchical task decomposition' - a key principle
in Agentic AI where complex problems are recursively broken into simpler subproblems.
This enables autonomous systems to tackle problems that would be impossible to solve
in a single step.
"""

from typing import List, Dict, Any
from datetime import datetime
import json


class PlannerAgent:
    """
    Plans research tasks by decomposing queries into actionable subtasks.
    
    Agentic AI Principle: Hierarchical Planning
    - Breaks complex goals into achievable steps
    - Each subtask can be executed independently by specialized agents
    - Creates a dependency graph for task execution order
    """
    
    def __init__(self, knowledge_graph=None):
        """
        Initialize the Planner Agent.
        
        Args:
            knowledge_graph: Reference to the knowledge graph for logging decisions
        """
        self.knowledge_graph = knowledge_graph
        self.name = "PlannerAgent"
    
    def plan(self, query: str) -> List[Dict[str, Any]]:
        """
        Decompose a research query into subtasks.
        
        Args:
            query: The research question or topic
            
        Returns:
            List of subtasks with metadata
            
        Educational Note:
        In a production system, this would use an LLM (like GroqCloud or GPT-4)
        to intelligently decompose tasks. This implementation uses heuristics
        to demonstrate the architecture pattern.
        """
        self._log_action("planning_started", {"query": query})
        
        subtasks = self._decompose_query(query)
        
        self._log_action("planning_completed", {
            "query": query,
            "subtask_count": len(subtasks),
            "subtasks": subtasks
        })
        
        return subtasks
    
    def _decompose_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Heuristic-based task decomposition.
        
        Educational Note:
        Real-world implementation would use LLM-based reasoning:
        - Analyze the query to identify key concepts
        - Generate search strategies
        - Determine what information sources are needed
        - Create a logical execution order
        """
        subtasks = [
            {
                "id": 1,
                "type": "search",
                "description": f"Search for current information about: {query}",
                "query": query,
                "priority": "high"
            },
            {
                "id": 2,
                "type": "search",
                "description": f"Find recent trends and developments related to: {query}",
                "query": f"recent trends {query}",
                "priority": "medium"
            },
            {
                "id": 3,
                "type": "search",
                "description": f"Gather expert opinions and analysis on: {query}",
                "query": f"expert analysis {query}",
                "priority": "medium"
            },
            {
                "id": 4,
                "type": "summarize",
                "description": "Synthesize all gathered information",
                "priority": "high",
                "depends_on": [1, 2, 3]
            },
            {
                "id": 5,
                "type": "write",
                "description": "Generate comprehensive research report",
                "priority": "high",
                "depends_on": [4]
            }
        ]
        
        return subtasks
    
    def _log_action(self, action: str, data: Dict[str, Any]):
        """Log planning actions to knowledge graph."""
        if self.knowledge_graph:
            self.knowledge_graph.log_agent_action(
                agent=self.name,
                action=action,
                data=data,
                timestamp=datetime.now().isoformat()
            )
