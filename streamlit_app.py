"""
Autonomous Research Agent - Streamlit GUI

A beautiful web interface for the Autonomous Research Agent demonstrating
Agentic AI Knowledge Architecture principles through an interactive GUI.
"""

import streamlit as st
import os
from datetime import datetime
from pathlib import Path

from agents import PlannerAgent, SearchAgent, SummarizerAgent, WriterAgent
from agents.config import config
from storage import KnowledgeGraph, VectorMemory
try:
    from utils import export_report_to_pdf, generate_all_visualizations
except ImportError:
    export_report_to_pdf = None
    generate_all_visualizations = None


st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def initialize_agent():
    """Initialize the research agent (cached to prevent reloading)."""
    knowledge_graph = KnowledgeGraph()
    vector_memory = VectorMemory()
    
    planner = PlannerAgent(knowledge_graph)
    searcher = SearchAgent(knowledge_graph)
    summarizer = SummarizerAgent(knowledge_graph)
    writer = WriterAgent(knowledge_graph)
    
    return {
        'knowledge_graph': knowledge_graph,
        'vector_memory': vector_memory,
        'planner': planner,
        'searcher': searcher,
        'summarizer': summarizer,
        'writer': writer
    }


def execute_research(query: str, components: dict):
    """Execute the autonomous research workflow with progress tracking."""
    
    kg = components['knowledge_graph']
    vm = components['vector_memory']
    planner = components['planner']
    searcher = components['searcher']
    summarizer = components['summarizer']
    writer = components['writer']
    
    session_id = kg.start_session(query)
    
    with st.status("🤖 Research in Progress...", expanded=True) as status:
        
        st.write("📋 **Phase 1: Planning**")
        with st.spinner("Breaking down the query into subtasks..."):
            subtasks = planner.plan(query)
            st.success(f"✓ Generated {len(subtasks)} subtasks")
        
        st.write("🔍 **Phase 2: Information Gathering**")
        with st.spinner("Searching web sources..."):
            search_results = []
            for subtask in subtasks:
                if subtask.get("type") == "search":
                    query_text = subtask.get("query", "")
                    results = searcher.search(query_text)
                    search_results.append(results)
                    st.write(f"   • Searched: {query_text} ({len(results)} results)")
            
            total_sources = sum(len(r) for r in search_results)
            st.success(f"✓ Collected {total_sources} sources")
        
        st.write("🧠 **Phase 3: Synthesis**")
        with st.spinner("Analyzing and synthesizing findings..."):
            summary = summarizer.summarize(search_results)
            key_findings_count = len(summary.get('key_findings', []))
            st.success(f"✓ Synthesized {key_findings_count} key findings")
        
        st.write("📝 **Phase 4: Report Generation**")
        with st.spinner("Writing comprehensive report..."):
            report = writer.write_report(query, summary)
            report_path = save_report(query, report)
            st.success(f"✓ Report generated")
        
        st.write("💾 **Phase 5: Memory Update**")
        with st.spinner("Updating memory systems..."):
            vm.store(
                text=query,
                metadata={
                    "type": "research_query",
                    "timestamp": datetime.now().isoformat(),
                    "key_findings_count": key_findings_count,
                    "source_count": summary.get("source_count", 0)
                }
            )
            
            for finding in summary.get("key_findings", [])[:5]:
                vm.store(
                    text=finding.get("point", ""),
                    metadata={
                        "type": "key_finding",
                        "query": query,
                        "source": finding.get("source", "Unknown"),
                        "timestamp": datetime.now().isoformat()
                    }
                )
            
            st.success("✓ Memory systems updated")
        
        status.update(label="✅ Research Complete!", state="complete")
    
    kg.end_session(session_id, "completed")
    
    return report, report_path


def save_report(query: str, report: str) -> str:
    """Save report to disk and return path."""
    os.makedirs("storage/reports", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = "".join(c if c.isalnum() else "_" for c in query)[:50]
    filename = f"report_{safe_query}_{timestamp}.md"
    filepath = os.path.join("storage/reports", filename)
    
    with open(filepath, 'w') as f:
        f.write(report)
    
    return filepath


def main():
    """Main Streamlit application."""
    
    st.title("🤖 Autonomous Research Agent")
    st.markdown("""
    *An educational demonstration of **Agentic AI Knowledge Architecture** principles*
    
    This system uses multiple specialized AI agents working together to conduct autonomous research:
    - 📋 **PlannerAgent** breaks queries into subtasks
    - 🔍 **SearchAgent** gathers information from the web
    - 🧠 **SummarizerAgent** synthesizes findings
    - 📝 **WriterAgent** generates comprehensive reports
    """)
    
    st.divider()
    
    components = initialize_agent()
    
    if 'selected_query' in st.session_state and st.session_state['selected_query']:
        st.session_state['query_text_input'] = st.session_state['selected_query']
        st.session_state['selected_query'] = ""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter Your Research Query")
        
        query = st.text_input(
            "What would you like to research?",
            placeholder="E.g., 2025 trends in open-source LLMs",
            label_visibility="collapsed",
            key="query_text_input"
        )
        
        st.markdown("**Quick Examples:**")
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("🤖 Open-source LLMs", use_container_width=True):
                st.session_state['selected_query'] = "2025 trends in open-source LLMs"
                st.rerun()
        
        with col_b:
            if st.button("🧠 Agentic AI", use_container_width=True):
                st.session_state['selected_query'] = "Latest developments in agentic AI systems"
                st.rerun()
        
        with col_c:
            if st.button("🚀 AI Applications", use_container_width=True):
                st.session_state['selected_query'] = "Autonomous agents in real-world applications"
                st.rerun()
    
    with col2:
        st.subheader("Agent Status")
        st.metric("Active Agents", "4")
        st.caption("PlannerAgent • SearchAgent • SummarizerAgent • WriterAgent")
    
    st.divider()
    
    if st.button("🚀 Run Research", type="primary", use_container_width=True, disabled=not query):
        if query:
            st.session_state['current_query'] = query
            
            report, report_path = execute_research(query, components)
            
            st.session_state['latest_report'] = report
            st.session_state['latest_report_path'] = report_path
            
            st.success("Research complete! View the report below.")
    
    if 'latest_report' in st.session_state:
        st.divider()
        st.subheader("📄 Generated Report")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.caption(f"Query: {st.session_state.get('current_query', 'N/A')}")
        with col2:
            with open(st.session_state['latest_report_path'], 'r') as f:
                st.download_button(
                    label="📄 Download MD",
                    data=f.read(),
                    file_name=Path(st.session_state['latest_report_path']).name,
                    mime="text/markdown",
                    use_container_width=True
                )
        with col3:
            if export_report_to_pdf:
                if st.button("📑 Export PDF", use_container_width=True):
                    try:
                        with st.spinner("Generating PDF..."):
                            pdf_path = export_report_to_pdf(
                                st.session_state['latest_report'],
                                st.session_state.get('current_query', 'report')
                            )
                        with open(pdf_path, 'rb') as f:
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=f.read(),
                                file_name=Path(pdf_path).name,
                                mime="application/pdf",
                                use_container_width=True
                            )
                        st.success("PDF generated!")
                    except Exception as e:
                        st.error(f"PDF generation failed: {e}")
        
        st.markdown(st.session_state['latest_report'])
    
    with st.sidebar:
        st.header("🤖 AI Configuration")
        
        config_status = config.get_status()
        llm_available = config_status['llm_available']
        
        if llm_available:
            st.success(f"✓ LLM Enabled ({config_status['llm_provider'].upper()})")
            st.caption(f"Model: {config_status['model']}")
        else:
            st.warning("⚠️ LLM Disabled (Basic Mode)")
            st.caption("Add GROQ_API_KEY or OPENAI_API_KEY to enable AI-powered features")
            with st.expander("How to add API keys"):
                st.markdown("""
                **Option 1: Using Secrets (Recommended)**
                1. Click the lock icon in the sidebar
                2. Add your API key:
                   - `GROQ_API_KEY` (Get free key at console.groq.com)
                   - `OPENAI_API_KEY` (Get at platform.openai.com)
                
                **Option 2: Environment Variables**
                Set `GROQ_API_KEY` or `OPENAI_API_KEY` in your Repl secrets
                """)
        
        st.divider()
        
        st.header("📊 System Statistics")
        
        kg_stats = components['knowledge_graph'].get_agent_stats()
        vm_stats = components['vector_memory'].get_stats()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sessions", kg_stats['total_sessions'])
            st.metric("Actions", kg_stats['total_actions'])
        with col2:
            st.metric("Agents", kg_stats['total_agents'])
            st.metric("Memories", vm_stats['total_vectors'])
        
        st.divider()
        
        st.subheader("🧠 Knowledge Graph")
        st.json({
            "total_sessions": kg_stats['total_sessions'],
            "total_actions": kg_stats['total_actions'],
            "active_agents": kg_stats['total_agents']
        })
        
        st.subheader("🗄️ Vector Memory")
        st.json({
            "stored_vectors": vm_stats['total_vectors'],
            "embedding_dim": vm_stats['embedding_dimension'],
            "storage_kb": round(vm_stats['storage_size_kb'], 2)
        })
        
        st.divider()
        
        st.subheader("📚 Recent Reports")
        reports_dir = Path("storage/reports")
        if reports_dir.exists():
            reports = sorted(reports_dir.glob("*.md"), key=os.path.getmtime, reverse=True)[:5]
            for report in reports:
                st.caption(f"📄 {report.name}")
        else:
            st.caption("No reports yet")
        
        st.divider()
        
        with st.expander("ℹ️ About"):
            st.markdown("""
            **Autonomous Research Agent**
            
            An educational project demonstrating Agentic AI Knowledge Architecture:
            
            - **Multi-Agent System**: Specialized agents work together
            - **Dual Memory**: Knowledge graph + vector store
            - **Autonomous**: No human intervention needed
            - **Transparent**: All actions logged
            
            Built with Python, LangChain, and Streamlit.
            """)


if __name__ == "__main__":
    main()
