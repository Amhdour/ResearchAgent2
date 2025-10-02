"""
Summarizer Agent - Information Synthesis

Role: Cognition Layer
Responsibility: Processes and condenses information from multiple sources

Educational Concept:
The Summarizer demonstrates 'information fusion' - combining data from
multiple sources into coherent knowledge. This is crucial in Agentic AI
for transforming raw data into actionable insights.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
try:
    from agents.config import config
except ImportError:
    config = None


class SummarizerAgent:
    """
    Synthesizes information from multiple sources into coherent summaries.
    
    Agentic AI Principle: Information Fusion & Synthesis
    - Combines data from disparate sources
    - Identifies key themes and patterns
    - Reduces information overload
    - Maintains source attribution
    """
    
    def __init__(self, knowledge_graph=None, use_llm=True):
        """
        Initialize the Summarizer Agent.
        
        Args:
            knowledge_graph: Reference to the knowledge graph for logging
            use_llm: Whether to use LLM for summarization (if available)
        """
        self.knowledge_graph = knowledge_graph
        self.name = "SummarizerAgent"
        self.use_llm = use_llm and config and config.enable_llm_summarization
        self.llm_client = config.get_llm_client() if self.use_llm else None
    
    def summarize(self, search_results: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Synthesize multiple search results into a structured summary.
        
        Args:
            search_results: List of search result lists from different queries
            
        Returns:
            Structured summary with key findings and sources
            
        Educational Note:
        In production, this would use LLM-based summarization (e.g., via GroqCloud).
        The LLM would:
        - Extract key concepts across sources
        - Identify agreements and contradictions
        - Generate coherent narrative summaries
        - Maintain factual accuracy with citations
        """
        self._log_action("summarization_started", {
            "source_count": len(search_results),
            "using_llm": self.use_llm and self.llm_client is not None
        })
        
        if self.llm_client:
            summary = self._synthesize_with_llm(search_results)
        else:
            summary = self._synthesize_information(search_results)
        
        self._log_action("summarization_completed", {
            "source_count": len(search_results),
            "key_points": len(summary.get("key_findings", [])),
            "method": "llm" if self.llm_client else "heuristic"
        })
        
        return summary
    
    def _synthesize_information(self, search_results: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Combine and structure information from multiple sources.
        
        Educational Note:
        This heuristic implementation demonstrates the pattern.
        Real implementation would use:
        - LLM-based extraction of key concepts
        - Semantic similarity to group related information
        - Citation tracking for source attribution
        - Fact-checking across multiple sources
        """
        all_results = []
        for result_list in search_results:
            all_results.extend(result_list)
        
        key_findings = []
        sources = []
        
        for result in all_results[:10]:
            key_findings.append({
                "point": result.get("snippet", "")[:200],
                "source": result.get("title", "Unknown"),
                "url": result.get("url", "")
            })
            
            if result.get("url"):
                sources.append({
                    "title": result.get("title", "Unknown"),
                    "url": result.get("url", "")
                })
        
        summary = {
            "key_findings": key_findings,
            "source_count": len(all_results),
            "sources": sources[:15],
            "synthesis_method": "heuristic_extraction"
        }
        
        return summary
    
    def _synthesize_with_llm(self, search_results: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Use LLM to synthesize information from multiple sources.
        
        This method uses a language model to:
        - Extract key insights across all sources
        - Identify patterns and themes
        - Generate coherent summaries with citations
        - Assess information quality and credibility
        """
        all_results = []
        for result_list in search_results:
            all_results.extend(result_list)
        
        if not all_results:
            return self._synthesize_information(search_results)
        
        context_parts = []
        for idx, result in enumerate(all_results[:15], 1):
            context_parts.append(
                f"Source {idx}: {result.get('title', 'Unknown')}\n"
                f"URL: {result.get('url', 'N/A')}\n"
                f"Content: {result.get('snippet', 'No description')}\n"
            )
        
        context = "\n".join(context_parts)
        
        prompt = f"""You are a research analyst synthesizing information from multiple sources.

Based on the following sources, extract and summarize the key findings:

{context}

Provide your analysis in the following JSON format:
{{
    "key_findings": [
        {{
            "point": "Key insight or finding",
            "source": "Source title",
            "url": "Source URL",
            "credibility": "high|medium|low"
        }}
    ],
    "summary": "Overall summary paragraph",
    "themes": ["theme1", "theme2"],
    "credibility_notes": "Notes on source reliability"
}}

Extract 5-8 key findings. Focus on factual information with proper attribution."""
        
        try:
            from langchain_core.messages import HumanMessage
            response = self.llm_client.invoke([HumanMessage(content=prompt)])
            
            import json
            result_text = response.content
            
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            llm_result = json.loads(result_text)
            
            sources = []
            for result in all_results[:15]:
                if result.get("url"):
                    sources.append({
                        "title": result.get("title", "Unknown"),
                        "url": result.get("url", "")
                    })
            
            return {
                "key_findings": llm_result.get("key_findings", []),
                "source_count": len(all_results),
                "sources": sources,
                "synthesis_method": "llm",
                "summary": llm_result.get("summary", ""),
                "themes": llm_result.get("themes", []),
                "credibility_notes": llm_result.get("credibility_notes", "")
            }
            
        except Exception as e:
            print(f"LLM synthesis failed: {e}. Falling back to heuristic method.")
            return self._synthesize_information(search_results)
    
    def _log_action(self, action: str, data: Dict[str, Any]):
        """Log summarization actions to knowledge graph."""
        if self.knowledge_graph:
            self.knowledge_graph.log_agent_action(
                agent=self.name,
                action=action,
                data=data,
                timestamp=datetime.now().isoformat()
            )
