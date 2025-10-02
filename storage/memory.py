"""
Vector Memory - Semantic Memory System

Role: Semantic Memory
Responsibility: Store and retrieve information based on meaning, not exact matches

Educational Concept:
Vector databases enable 'semantic search' - finding information based on
meaning rather than keywords. This is crucial for Agentic AI to:
- Learn from past experiences
- Find relevant context for new problems
- Build knowledge incrementally over time
"""

import os
import json
from typing import List, Dict, Any
import numpy as np


class VectorMemory:
    """
    Manages semantic memory using vector embeddings.
    
    Agentic AI Principle: Semantic Memory & Learning
    - Stores experiences as vector embeddings
    - Retrieves relevant past experiences for new problems
    - Enables learning and adaptation over time
    
    Educational Note:
    This is a simplified implementation. In production, you would use:
    - FAISS for efficient similarity search
    - Sentence-transformers for quality embeddings
    - Proper vector indexing for scale
    """
    
    def __init__(self, storage_path: str = "storage/vector_store"):
        """
        Initialize the Vector Memory.
        
        Args:
            storage_path: Directory for storing vectors and metadata
        """
        self.storage_path = storage_path
        self.vectors = []
        self.metadata = []
        os.makedirs(storage_path, exist_ok=True)
        self._load()
    
    def store(self, text: str, metadata: Dict[str, Any]):
        """
        Store text with its vector embedding.
        
        Args:
            text: The text to store
            metadata: Associated metadata (agent, action, timestamp, etc.)
            
        Educational Note:
        In production, this would:
        1. Generate embeddings using sentence-transformers or OpenAI
        2. Store in FAISS index for efficient retrieval
        3. Maintain metadata in separate database
        """
        vector = self._simple_embedding(text)
        
        self.vectors.append(vector)
        self.metadata.append({
            "text": text,
            "embedding_dim": len(vector),
            **metadata
        })
        
        self._save()
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Find semantically similar past experiences.
        
        Args:
            query: Query text
            top_k: Number of results to return
            
        Returns:
            List of similar experiences with metadata
            
        Educational Note:
        Real implementation would use:
        - FAISS for fast approximate nearest neighbor search
        - Quality embedding models for semantic understanding
        - Filtering by metadata (agent, time range, etc.)
        """
        if not self.vectors:
            return []
        
        query_vector = self._simple_embedding(query)
        
        similarities = []
        for idx, stored_vector in enumerate(self.vectors):
            similarity = self._cosine_similarity(query_vector, stored_vector)
            similarities.append((idx, similarity))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        results = []
        for idx, score in similarities[:top_k]:
            result = self.metadata[idx].copy()
            result["similarity_score"] = float(score)
            results.append(result)
        
        return results
    
    def _simple_embedding(self, text: str) -> List[float]:
        """
        Create a simple embedding for educational purposes.
        
        Educational Note:
        This uses a very basic character-frequency approach.
        In production, use:
        - sentence-transformers: all-MiniLM-L6-v2 (fast, good quality)
        - OpenAI ada-002 (high quality, API-based)
        - HuggingFace models (various options)
        """
        text = text.lower()
        
        embedding = [0.0] * 128
        
        for i, char in enumerate(text[:128]):
            embedding[i] = ord(char) / 256.0
        
        text_hash = hash(text) % 128
        embedding[text_hash] = 1.0
        
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = [float(x / norm) for x in embedding]
        
        return embedding
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        arr1 = np.array(vec1)
        arr2 = np.array(vec2)
        
        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def _save(self):
        """Persist vector store to disk."""
        try:
            data = {
                "vectors": [vec for vec in self.vectors],
                "metadata": self.metadata
            }
            
            with open(os.path.join(self.storage_path, "vectors.json"), 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save vector store: {e}")
    
    def _load(self):
        """Load vector store from disk."""
        vector_file = os.path.join(self.storage_path, "vectors.json")
        if os.path.exists(vector_file):
            try:
                with open(vector_file, 'r') as f:
                    data = json.load(f)
                    self.vectors = data.get("vectors", [])
                    self.metadata = data.get("metadata", [])
            except Exception as e:
                print(f"Warning: Could not load vector store: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        return {
            "total_vectors": len(self.vectors),
            "embedding_dimension": len(self.vectors[0]) if self.vectors else 0,
            "storage_size_kb": os.path.getsize(os.path.join(self.storage_path, "vectors.json")) / 1024 if os.path.exists(os.path.join(self.storage_path, "vectors.json")) else 0
        }
