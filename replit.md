# Autonomous Research Agent

## Overview

An educational autonomous research system demonstrating Agentic AI Knowledge Architecture principles. The system orchestrates multiple specialized AI agents to conduct research autonomously - receiving queries, planning tasks, gathering web information, synthesizing findings, and generating comprehensive reports. The project serves as a learning tool for understanding how modern autonomous AI systems work through a practical implementation.

## User Preferences

Preferred communication style: Simple, everyday language.

## Replit Environment Setup

This project has been successfully configured for the Replit environment with the following setup:

**Web Interface**
- Primary interface: Streamlit web GUI accessible via Replit's webview
- Configured to run on port 5000 with address 0.0.0.0
- Streamlit config at `.streamlit/config.toml` enables headless mode for deployment

**Workflow Configuration**
- Automated workflow launches `streamlit_app.py` on startup
- All dependencies managed via `pyproject.toml` and installed automatically with `uv`
- Python 3.11 environment configured

**Deployment**
- Configured for autoscale deployment (suitable for web applications)
- Production deployment command: `streamlit run streamlit_app.py --server.port 5000 --server.address 0.0.0.0 --server.headless`
- No API keys required for basic functionality (uses DuckDuckGo search)
- Optional: Add GROQ_API_KEY or OPENAI_API_KEY for AI-powered features

**Storage**
- All generated reports saved to `storage/reports/`
- Knowledge graph persisted to `storage/knowledge_graph.json`
- Vector memory stored in `storage/vector_store/`

## AI-Powered Features (NEW)

### LLM Integration
- **Smart Summarization**: Uses Groq or OpenAI LLMs to analyze and synthesize research findings
- **Intelligent Report Generation**: Creates professional, well-structured reports with LLM assistance
- **Automatic Fallback**: Works in basic mode without API keys, uses LLM when available
- **Supported Providers**: Groq (llama-3.3-70b-versatile), OpenAI (GPT-4)
- **Configuration**: Add API keys via Replit secrets (GROQ_API_KEY or OPENAI_API_KEY)

### Enhanced Search Capabilities
- **Multi-Source Search**: Combines web and news results for comprehensive coverage
- **News Integration**: Dedicated news search for recent developments
- **Result Deduplication**: Automatically removes duplicate sources
- **Source Credibility**: LLM-powered credibility assessment for sources
- **Date-Aware**: News results include publication dates

### Advanced Report Features
- **PDF Export**: Convert reports to professional PDF documents with one click
- **Visualizations**: Generate charts showing source distribution and credibility analysis
- **Theme Analysis**: LLM extracts and visualizes key themes from research
- **Enhanced Formatting**: Professional layouts with proper citations

### User Interface Enhancements
- **AI Status Indicator**: Shows whether LLM features are enabled
- **Configuration Guide**: In-app instructions for adding API keys
- **Download Options**: Both Markdown and PDF export available
- **Progress Tracking**: Real-time status updates during research

## System Architecture

### Multi-Agent Architecture Pattern

The system implements a **hierarchical multi-agent orchestration** pattern where specialized agents collaborate autonomously:

- **Orchestrator** (`AutonomousResearchAgent`): Central coordinator managing the research workflow and agent interactions
- **Agent Specialization**: Each agent has a single, well-defined responsibility following the Single Responsibility Principle
- **Layered Architecture**: Agents are organized into functional layers (perception, cognition, action) mapping to cognitive architecture concepts

**Design Rationale**: Modular agent design enables independent development, testing, and enhancement of each capability. This mirrors real cognitive systems where specialized modules handle different aspects of intelligence.

### Agent Roles & Responsibilities

**Cognition Layer - Planning**
- `PlannerAgent`: Decomposes complex research queries into manageable subtasks using hierarchical task decomposition
- Implements dependency-aware task sequencing
- Currently uses rule-based planning; designed to integrate LLM-based planning in production

**Perception Layer - Information Gathering**
- `SearchAgent`: Interfaces with external knowledge sources (DuckDuckGo Search API)
- Handles web search execution, error recovery, and result structuring
- Transforms unstructured web data into standardized formats for downstream processing

**Cognition Layer - Synthesis**
- `SummarizerAgent`: Fuses information from multiple sources into coherent knowledge
- Performs multi-source data aggregation and theme extraction
- Designed for LLM-based summarization integration

**Action Layer - Output Generation**
- `WriterAgent`: Transforms synthesized knowledge into human-readable Markdown reports
- Handles formatting, structure, and presentation of research findings

**Trade-offs**: The multi-agent approach adds complexity versus monolithic design, but provides superior modularity, testability, and extensibility for educational purposes.

### Dual Memory Architecture

The system implements two complementary memory systems reflecting human cognitive architecture:

**Episodic Memory - Knowledge Graph**
- **Implementation**: JSON-based structured log (`KnowledgeGraph` class)
- **Purpose**: Tracks all agent actions, decisions, reasoning steps, and temporal sequences
- **Storage**: `storage/knowledge_graph.json`
- **Key Features**:
  - Session-based organization
  - Agent activity logging
  - Decision audit trail
  - Temporal reasoning support

**Semantic Memory - Vector Store**
- **Implementation**: Vector embedding storage (`VectorMemory` class)
- **Purpose**: Enables meaning-based information retrieval and learning from past experiences
- **Storage**: `storage/vector_store/` directory
- **Key Features**:
  - Simplified vector similarity search
  - Experience storage and retrieval
  - Designed for FAISS/Chroma integration in production

**Design Rationale**: Dual memory enables both explainability (through structured logs) and semantic learning (through vector retrieval). This combination supports debugging, trust-building, and continuous improvement.

### User Interface

The system provides two interfaces:

**Streamlit Web GUI** (Primary Interface)
- **Implementation**: `streamlit_app.py` running on port 5000
- **Features**:
  - Interactive query input with quick example buttons
  - Real-time progress tracking through research phases
  - Markdown report viewer with download functionality
  - Live statistics sidebar showing memory systems and session history
  - Beautiful, educational UI demonstrating agent workflow
- **Access**: Runs automatically via Replit workflow

**Command Line Interface** (Development Interface)
- **Implementation**: `main.py`
- **Features**: Interactive menu, console progress indicators, batch processing
- **Use Case**: Debugging, scripting, headless operation

### Data Flow Architecture

1. **Input Processing**: User query received via web GUI or CLI interface
2. **Planning Phase**: PlannerAgent decomposes query into subtasks
3. **Execution Phase**: SearchAgent executes each subtask, gathering web data
4. **Synthesis Phase**: SummarizerAgent fuses multi-source information
5. **Output Phase**: WriterAgent generates final Markdown report
6. **Memory Recording**: All activities logged to both knowledge graph and vector store

### Error Handling & Resilience

- **Graceful Degradation**: Search failures handled with fallback messages
- **Retry Logic**: Built into SearchAgent for API failures
- **Validation**: Input validation and sanitization at entry points
- **Logging**: Comprehensive activity logging for debugging

### Educational Design Principles

**Code Organization**
- Clear module separation (`agents/`, `storage/`, `examples/`)
- Extensive inline documentation explaining AI concepts
- Type hints throughout for clarity

**Extensibility Points**
- Agent classes designed for LLM integration (Groq, OpenAI, HuggingFace)
- Pluggable memory backends (current JSON → production FAISS/Chroma)
- Tool registry pattern for adding new agent capabilities

**Learning Scaffolding**
- Comments explain "why" not just "what"
- Example queries provided with expected behaviors
- README maps code to theoretical concepts

## External Dependencies

### Core Libraries

**AI/ML Stack**
- `duckduckgo-search`: Web search API for information retrieval (perception layer)
- Designed for integration with: LangChain, LlamaIndex, or CrewAI (not yet implemented)
- Target LLM providers: GroqCloud (primary), HuggingFace (fallback)

**User Interface**
- `rich`: Terminal UI library for formatted console output, progress indicators, and markdown rendering
- Provides panels, progress bars, spinners, and markdown display

**Data Processing**
- `numpy`: Vector operations for simplified semantic memory
- Standard library `json`: Knowledge graph serialization
- Production targets: FAISS or Chroma for vector databases

### External Services

**Search API**
- DuckDuckGo Search (via `duckduckgo-search` library)
- No authentication required
- Rate limiting handled internally

**Future LLM Integration Points**
- GroqCloud API (planned for production agent reasoning)
- HuggingFace Inference API (fallback option)
- Requires API key configuration via environment variables

### File System Storage

**Persistent Storage**
- `storage/knowledge_graph.json`: Episodic memory persistence
- `storage/vector_store/`: Semantic memory vectors and metadata
- `storage/reports/`: Generated research reports (markdown)

**Configuration**
- No external configuration files required
- Storage paths configurable via class constructors
- Environment variables for future API key management

### Python Version & Environment

- **Requirement**: Python 3.11+
- **Deployment Target**: Replit environment
- **Package Management**: pip (requirements.txt or pyproject.toml)