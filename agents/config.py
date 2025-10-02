"""
Agent Configuration - LLM Integration Settings

Manages API keys, model settings, and feature flags for the autonomous research agent.
"""

import os
from typing import Optional, Dict, Any
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    GROQ = "groq"
    OPENAI = "openai"
    NONE = "none"


class AgentConfig:
    """
    Central configuration for AI-powered features.
    
    Features:
    - LLM integration for summarization and report generation
    - API key management through environment variables
    - Model selection and configuration
    - Feature flags for enhanced capabilities
    """
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.llm_provider = self._get_llm_provider()
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        self.groq_model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.openai_model = os.environ.get("OPENAI_MODEL", "gpt-4")
        
        self.enable_llm_summarization = self._check_llm_available()
        self.enable_llm_writing = self._check_llm_available()
        
        self.enable_pdf_export = True
        self.enable_visualizations = True
        self.enable_credibility_scoring = True
        
    def _get_llm_provider(self) -> LLMProvider:
        """Determine which LLM provider to use based on available API keys."""
        provider = os.environ.get("LLM_PROVIDER", "").lower()
        
        if provider == "groq":
            return LLMProvider.GROQ
        elif provider == "openai":
            return LLMProvider.OPENAI
        elif provider == "none":
            return LLMProvider.NONE
        
        if os.environ.get("GROQ_API_KEY"):
            return LLMProvider.GROQ
        elif os.environ.get("OPENAI_API_KEY"):
            return LLMProvider.OPENAI
        else:
            return LLMProvider.NONE
    
    def _check_llm_available(self) -> bool:
        """Check if LLM is available for use."""
        if self.llm_provider == LLMProvider.GROQ:
            return bool(self.groq_api_key)
        elif self.llm_provider == LLMProvider.OPENAI:
            return bool(self.openai_api_key)
        return False
    
    def get_llm_client(self):
        """
        Get the appropriate LLM client based on configuration.
        
        Returns:
            Configured LangChain LLM instance or None
        """
        if not self.enable_llm_summarization:
            return None
        
        try:
            if self.llm_provider == LLMProvider.GROQ:
                from langchain_groq import ChatGroq
                return ChatGroq(
                    model=self.groq_model,
                    temperature=0.3,
                    max_retries=2,
                    api_key=self.groq_api_key
                )
            elif self.llm_provider == LLMProvider.OPENAI:
                from langchain_openai import ChatOpenAI
                return ChatOpenAI(
                    model=self.openai_model,
                    temperature=0.3,
                    api_key=self.openai_api_key
                )
        except Exception as e:
            print(f"Failed to initialize LLM client: {e}")
            return None
        
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get current configuration status."""
        return {
            "llm_provider": self.llm_provider.value,
            "llm_available": self.enable_llm_summarization,
            "model": self.groq_model if self.llm_provider == LLMProvider.GROQ else self.openai_model,
            "features": {
                "llm_summarization": self.enable_llm_summarization,
                "llm_writing": self.enable_llm_writing,
                "pdf_export": self.enable_pdf_export,
                "visualizations": self.enable_visualizations,
                "credibility_scoring": self.enable_credibility_scoring
            }
        }


config = AgentConfig()
