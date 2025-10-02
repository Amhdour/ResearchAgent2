"""
Storage Module - Memory and Knowledge Management

This module implements the 'memory' component of Agentic AI Knowledge Architecture.
Autonomous agents need both:
- Episodic memory (what happened when) - implemented via knowledge graph
- Semantic memory (what do things mean) - implemented via vector database

Educational Note:
Human intelligence relies on multiple memory systems. Similarly, effective
Agentic AI requires structured (knowledge graph) and unstructured (vector)
memory to function autonomously.
"""

from .knowledge_graph import KnowledgeGraph
from .memory import VectorMemory

__all__ = ['KnowledgeGraph', 'VectorMemory']
