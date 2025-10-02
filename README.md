# Autonomous Research Agent

An educational project demonstrating **Agentic AI Knowledge Architecture** principles through a working autonomous research system.

## 🎯 Project Overview

This project implements a multi-agent autonomous research system that:
- Receives research queries from users
- Plans and executes research autonomously
- Gathers information from web sources
- Synthesizes findings into comprehensive reports
- Maintains memory of all actions for learning and improvement

## 🧠 Agentic AI Knowledge Architecture

This project demonstrates the core components of modern Agentic AI systems:

### 1. **Perception Layer** (SearchAgent)
Gathers information from external sources (web search, APIs, databases). Just as humans perceive through senses, AI agents perceive through tools.

### 2. **Cognition Layer** (PlannerAgent, SummarizerAgent)
- **Planning**: Breaks complex goals into manageable subtasks
- **Synthesis**: Combines information from multiple sources into coherent knowledge
- **Reasoning**: Determines optimal strategies for achieving goals

### 3. **Memory Systems**
- **Knowledge Graph** (Episodic Memory): Tracks what happened, when, and why
- **Vector Database** (Semantic Memory): Stores meaning and enables semantic retrieval

### 4. **Action Layer** (WriterAgent)
Produces outputs and interacts with the external world through report generation.

## 📁 Project Structure

```
.
├── agents/                    # Specialized agent modules
│   ├── __init__.py
│   ├── planner.py            # Task decomposition & orchestration
│   ├── search.py             # Web search & information retrieval
│   ├── summarizer.py         # Information synthesis
│   └── writer.py             # Report generation
│
├── storage/                   # Persistent memory systems
│   ├── __init__.py
│   ├── knowledge_graph.py    # Episodic memory (structured)
│   ├── memory.py             # Semantic memory (vector-based)
│   ├── knowledge_graph.json  # Generated: action logs
│   └── vector_store/         # Generated: embeddings
│
├── examples/                  # Sample research queries
│   └── example_queries.md    # Demo prompts & expected outputs
│
├── main.py                    # Main entry point & orchestrator
└── README.md                  # This file
```

## 🚀 Getting Started

### Prerequisites

This project runs on Replit with Python 3.11+ and the following dependencies:
- `langchain` - Agent orchestration
- `langchain-community` - Community tools & integrations
- `duckduckgo-search` - Web search without API keys
- `rich` - Beautiful CLI output
- `pydantic` - Data validation
- `numpy` - Vector operations

### Installation on Replit

1. **Fork/Clone this Repl**
2. **Dependencies are auto-installed** - Replit handles package management
3. **Run the agent:**
   ```bash
   python main.py
   ```

### Running Research Queries

The CLI provides an interactive menu:

```
1. 2025 trends in open-source LLMs
2. Latest developments in agentic AI systems
3. Autonomous agents in real-world applications
4. Custom query
5. Show statistics
0. Exit
```

Select an option and the agent will autonomously:
1. Plan the research approach
2. Execute web searches
3. Synthesize findings
4. Generate a comprehensive report
5. Store results in memory

## 📊 Output Files

### Research Reports
- **Location**: `storage/reports/`
- **Format**: Markdown (.md)
- **Contents**: Executive summary, key findings, sources

### Knowledge Graph
- **Location**: `storage/knowledge_graph.json`
- **Purpose**: Tracks all agent actions, decisions, and reasoning
- **Use Case**: Debugging, analysis, learning from past sessions

### Vector Store
- **Location**: `storage/vector_store/`
- **Purpose**: Semantic memory for finding relevant past experiences
- **Use Case**: Learning, context retrieval, pattern recognition

## 🎓 Educational Concepts

### What is Agentic AI?

**Agentic AI** refers to systems that can:
- Act autonomously toward goals
- Plan multi-step strategies
- Use tools and external resources
- Learn from experience
- Explain their reasoning

### Key Principles Demonstrated

1. **Autonomous Operation**
   - Agents work without human intervention at each step
   - System decomposes complex tasks automatically

2. **Specialized Agents**
   - Each agent has a focused responsibility
   - Agents collaborate through clear interfaces

3. **Memory & Learning**
   - Knowledge graph provides audit trail
   - Vector store enables semantic learning

4. **Tool Use**
   - Agents interact with external systems (web search)
   - Handles errors and retries gracefully

5. **Transparency**
   - All decisions logged to knowledge graph
   - Explainable AI through memory inspection

## 🔧 Extending the Project

### Adding New Agents

Create a new agent in `agents/` following this pattern:

```python
class YourAgent:
    def __init__(self, knowledge_graph=None):
        self.knowledge_graph = knowledge_graph
        self.name = "YourAgent"
    
    def your_method(self, input_data):
        self._log_action("action_name", {"data": input_data})
        # Your logic here
        return result
    
    def _log_action(self, action, data):
        if self.knowledge_graph:
            self.knowledge_graph.log_agent_action(
                agent=self.name,
                action=action,
                data=data,
                timestamp=datetime.now().isoformat()
            )
```

### Integrating LLMs (GroqCloud, HuggingFace, OpenAI)

The current implementation uses heuristics for planning, summarization, and writing. To integrate real LLMs:

#### Option 1: GroqCloud (Fast, Open Models)
```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key="your_groq_api_key",
    model_name="mixtral-8x7b-32768"
)
```

#### Option 2: HuggingFace (Local/API Models)
```python
from langchain_huggingface import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-2-7b-chat-hf",
    huggingfacehub_api_token="your_token"
)
```

#### Option 3: OpenAI (High Quality)
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key="your_openai_key",
    model="gpt-4"
)
```

Then update agents to use the LLM:
```python
# In SummarizerAgent
def summarize(self, search_results):
    prompt = f"Summarize these research findings: {search_results}"
    response = self.llm.invoke(prompt)
    return response.content
```

### Adding Better Embeddings

Replace the simple embedding in `storage/memory.py`:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def _simple_embedding(self, text):
    return model.encode(text).tolist()
```

### Adding FAISS for Scalable Vector Search

```python
import faiss

# Create FAISS index
dimension = 384  # for all-MiniLM-L6-v2
index = faiss.IndexFlatL2(dimension)

# Add vectors
index.add(np.array(vectors))

# Search
distances, indices = index.search(query_vector, k=5)
```

## 🔍 Understanding the Workflow

### Autonomous Research Loop

```
User Query → PlannerAgent → [Subtask1, Subtask2, ...]
                ↓
         SearchAgent (executes searches)
                ↓
         SummarizerAgent (combines findings)
                ↓
         WriterAgent (generates report)
                ↓
         Memory Systems (store for future use)
                ↓
         Report delivered to user
```

### Knowledge Graph Structure

```json
{
  "metadata": {
    "created": "timestamp",
    "version": "1.0.0"
  },
  "sessions": [
    {
      "id": "session_1",
      "query": "research query",
      "started": "timestamp",
      "status": "completed",
      "actions": [...]
    }
  ],
  "agents": {
    "PlannerAgent": {
      "first_seen": "timestamp",
      "action_count": 10
    }
  },
  "actions": [...]
}
```

## 🐛 Troubleshooting

### Web Search Issues
- DuckDuckGo search may occasionally time out
- System includes retry logic and error handling
- Rate limits apply - agent includes delays

### Memory Storage
- JSON files created in `storage/` directory
- Ensure write permissions in storage folders
- Files are auto-created on first run

### Performance
- Simple embeddings are intentionally basic for education
- For production, use sentence-transformers or OpenAI embeddings
- FAISS significantly improves search speed at scale

## 📚 Learn More

### Recommended Reading
- [LangChain Documentation](https://python.langchain.com/)
- [Agentic AI Patterns](https://www.anthropic.com/research)
- [Vector Databases Explained](https://www.pinecone.io/learn/)
- [Knowledge Graphs in AI](https://neo4j.com/developer/knowledge-graph/)

### Related Concepts
- Multi-agent systems
- Tool-using AI (function calling)
- Retrieval-Augmented Generation (RAG)
- Semantic search and embeddings
- LLM orchestration frameworks

## 📄 License

This is an educational project. Feel free to use, modify, and learn from it.

## 🤝 Contributing

This project is designed for learning. Suggestions for improvements:
- Add more sophisticated planning algorithms
- Integrate additional search sources
- Implement agent collaboration patterns
- Add evaluation metrics for research quality
- Create visualization tools for knowledge graph

---

**Built for educational purposes to demonstrate Agentic AI Knowledge Architecture principles (2025)**
