# Example Research Queries

This file contains sample research queries to demonstrate the Autonomous Research Agent's capabilities.

## Example 1: Emerging Technology Trends
**Query:** "2025 trends in open-source LLMs"

**Expected Output:**
- Recent developments in open-source language models
- Key players and frameworks (Llama, Mistral, etc.)
- Trends in model efficiency and accessibility
- Community adoption patterns

## Example 2: Agentic AI Systems
**Query:** "Latest developments in agentic AI systems"

**Expected Output:**
- Current state of autonomous agents
- Integration patterns with LLMs
- Tool use and function calling capabilities
- Real-world applications and case studies

## Example 3: Practical Applications
**Query:** "Autonomous agents in real-world applications"

**Expected Output:**
- Industry use cases (customer service, research, automation)
- Success stories and implementations
- Challenges and limitations
- Best practices for deployment

## How to Run These Examples

Using the CLI:
```bash
python main.py
```

Then select from the menu:
1. Option 1, 2, or 3 for pre-configured examples
2. Option 4 to enter your own custom query
3. Option 5 to view system statistics

## Understanding the Output

Each research session generates:
1. **Markdown Report** - Saved in `storage/reports/`
2. **Knowledge Graph Entry** - Logged in `storage/knowledge_graph.json`
3. **Vector Embeddings** - Stored in `storage/vector_store/`

## Customizing Queries

For best results, structure your queries to be:
- **Specific** - Include key terms and context
- **Time-bounded** - Reference current year for latest info
- **Focused** - One main topic per query
- **Open-ended** - Allow for comprehensive exploration

## Educational Notes

### What Happens During Research:

1. **Planning Phase** (PlannerAgent)
   - Query is decomposed into subtasks
   - Search strategies are determined
   - Execution order is planned

2. **Search Phase** (SearchAgent)
   - Multiple searches executed
   - Results gathered from web sources
   - Data structured for processing

3. **Synthesis Phase** (SummarizerAgent)
   - Information from multiple sources combined
   - Key findings extracted
   - Sources tracked for attribution

4. **Writing Phase** (WriterAgent)
   - Comprehensive report generated
   - Markdown formatting applied
   - Citations included

5. **Memory Phase** (Storage Systems)
   - Knowledge graph updated
   - Vector embeddings stored
   - Statistics tracked

### Agentic AI Principles Demonstrated:

- **Autonomy** - Agents work without human intervention
- **Specialization** - Each agent has a focused role
- **Collaboration** - Agents share information via orchestrator
- **Memory** - Past experiences inform future actions
- **Transparency** - All decisions are logged
