"""
Knowledge Graph - Structured Memory System

Role: Episodic Memory
Responsibility: Track all agent actions, decisions, and reasoning steps

Educational Concept:
The Knowledge Graph provides 'explainability' and 'auditability' for
autonomous systems. Every decision is logged with context, enabling:
- Debugging of agent behavior
- Learning from past experiences
- Building trust through transparency
"""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import os


class KnowledgeGraph:
    """
    Maintains a structured log of all agent activities.
    
    Agentic AI Principle: Explainable AI Through Memory
    - Tracks decision-making processes
    - Enables post-hoc analysis of agent behavior
    - Provides foundation for learning and improvement
    - Supports debugging and verification
    """
    
    def __init__(self, storage_path: str = "storage/knowledge_graph.json"):
        """
        Initialize the Knowledge Graph.
        
        Args:
            storage_path: Path to the JSON file storing the graph
        """
        self.storage_path = storage_path
        self.graph = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "version": "1.0.0",
                "description": "Autonomous Research Agent Knowledge Graph"
            },
            "sessions": [],
            "agents": {},
            "actions": []
        }
        self.current_session_id = None
        self._load()
    
    def start_session(self, query: str) -> str:
        """
        Begin a new research session.
        
        Args:
            query: The research query for this session
            
        Returns:
            Session ID
        """
        session_id = f"session_{len(self.graph['sessions']) + 1}_{int(datetime.now().timestamp())}"
        
        session = {
            "id": session_id,
            "query": query,
            "started": datetime.now().isoformat(),
            "status": "active",
            "actions": []
        }
        
        self.graph["sessions"].append(session)
        self.current_session_id = session_id
        self._save()
        
        return session_id
    
    def end_session(self, session_id: str, status: str = "completed"):
        """
        Complete a research session.
        
        Args:
            session_id: The session to end
            status: Final status (completed, failed, cancelled)
        """
        for session in self.graph["sessions"]:
            if session["id"] == session_id:
                session["ended"] = datetime.now().isoformat()
                session["status"] = status
                break
        
        self._save()
    
    def log_agent_action(self, agent: str, action: str, data: Dict[str, Any], timestamp: Optional[str] = None):
        """
        Log an agent action to the knowledge graph.
        
        Args:
            agent: Name of the agent performing the action
            action: Type of action performed
            data: Action-specific data and results
            timestamp: ISO timestamp (auto-generated if not provided)
            
        Educational Note:
        This is the core of agent observability. Every action is recorded,
        creating a complete audit trail of autonomous behavior.
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        action_entry = {
            "agent": agent,
            "action": action,
            "timestamp": timestamp,
            "session_id": self.current_session_id,
            "data": data
        }
        
        self.graph["actions"].append(action_entry)
        
        if self.current_session_id:
            for session in self.graph["sessions"]:
                if session["id"] == self.current_session_id:
                    session["actions"].append(action_entry)
                    break
        
        if agent not in self.graph["agents"]:
            self.graph["agents"][agent] = {
                "first_seen": timestamp,
                "action_count": 0
            }
        
        self.graph["agents"][agent]["action_count"] += 1
        self.graph["agents"][agent]["last_seen"] = timestamp
        
        self._save()
    
    def get_session_history(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve the complete history of a session.
        
        Args:
            session_id: Session to retrieve (uses current if not specified)
            
        Returns:
            Session data with all actions
        """
        target_session_id = session_id or self.current_session_id
        
        for session in self.graph["sessions"]:
            if session["id"] == target_session_id:
                return session
        
        return {}
    
    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics about agent activity."""
        return {
            "total_agents": len(self.graph["agents"]),
            "total_actions": len(self.graph["actions"]),
            "total_sessions": len(self.graph["sessions"]),
            "agents": self.graph["agents"]
        }
    
    def _load(self):
        """Load knowledge graph from disk."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    loaded_graph = json.load(f)
                    self.graph.update(loaded_graph)
            except Exception as e:
                print(f"Warning: Could not load knowledge graph: {e}")
    
    def _save(self):
        """Persist knowledge graph to disk."""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(self.graph, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save knowledge graph: {e}")
