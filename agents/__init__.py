"""
Agents Module - Autonomous Research Agent System

This module contains specialized agents that work together to conduct autonomous research.
Each agent has a specific role in the Agentic AI Knowledge Architecture:

- PlannerAgent: Cognition layer - breaks down research queries into subtasks
- SearchAgent: Perception layer - gathers information from external sources
- SummarizerAgent: Cognition layer - processes and condenses information
- WriterAgent: Action layer - generates final research reports

Educational Note:
This demonstrates the core principle of Agentic AI: specialized components
working together autonomously to achieve complex goals.
"""

from .planner import PlannerAgent
from .search import SearchAgent
from .summarizer import SummarizerAgent
from .writer import WriterAgent

__all__ = ['PlannerAgent', 'SearchAgent', 'SummarizerAgent', 'WriterAgent']
