"""
Autonomous Research Agent - Main Entry Point

This is the orchestrator that brings all components together to demonstrate
Agentic AI Knowledge Architecture principles.

Architecture Overview:
1. Perception: SearchAgent gathers information from external sources
2. Cognition: PlannerAgent and SummarizerAgent process and synthesize
3. Memory: KnowledgeGraph (episodic) and VectorMemory (semantic)
4. Action: WriterAgent produces deliverables

Educational Goal:
Demonstrate how autonomous agents work together to achieve complex goals
without human intervention at each step.
"""

import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich import print as rprint

from agents import PlannerAgent, SearchAgent, SummarizerAgent, WriterAgent
from storage import KnowledgeGraph, VectorMemory


class AutonomousResearchAgent:
    """
    Main orchestrator for autonomous research.
    
    Agentic AI Architecture:
    - Coordinates multiple specialized agents
    - Manages persistent memory systems
    - Executes autonomous task loops
    - Provides transparency through logging
    """
    
    def __init__(self):
        """Initialize the autonomous research system."""
        self.console = Console()
        
        self.console.print(Panel.fit(
            "[bold cyan]Autonomous Research Agent[/bold cyan]\n"
            "Demonstrating Agentic AI Knowledge Architecture",
            border_style="cyan"
        ))
        
        self.knowledge_graph = KnowledgeGraph()
        self.vector_memory = VectorMemory()
        
        self.planner = PlannerAgent(self.knowledge_graph)
        self.searcher = SearchAgent(self.knowledge_graph)
        self.summarizer = SummarizerAgent(self.knowledge_graph)
        self.writer = WriterAgent(self.knowledge_graph)
        
        self.console.print("[green]✓[/green] All agents initialized")
        self.console.print("[green]✓[/green] Memory systems ready\n")
    
    def research(self, query: str) -> str:
        """
        Execute autonomous research workflow.
        
        Args:
            query: Research question or topic
            
        Returns:
            Path to generated report
            
        Educational Note:
        This is the autonomous loop:
        1. Plan: Break down the query into subtasks
        2. Execute: Run each subtask autonomously
        3. Synthesize: Combine results
        4. Deliver: Generate final output
        5. Remember: Store in memory for future use
        """
        self.console.print(f"\n[bold]Research Query:[/bold] {query}\n")
        
        session_id = self.knowledge_graph.start_session(query)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task1 = progress.add_task("[cyan]Planning research tasks...", total=None)
            subtasks = self.planner.plan(query)
            progress.update(task1, completed=True)
            self.console.print(f"[green]✓[/green] Generated {len(subtasks)} subtasks\n")
            
            task2 = progress.add_task("[cyan]Gathering information...", total=None)
            search_results = self._execute_searches(subtasks)
            progress.update(task2, completed=True)
            self.console.print(f"[green]✓[/green] Collected {sum(len(r) for r in search_results)} sources\n")
            
            task3 = progress.add_task("[cyan]Synthesizing findings...", total=None)
            summary = self.summarizer.summarize(search_results)
            progress.update(task3, completed=True)
            self.console.print(f"[green]✓[/green] Synthesized {len(summary.get('key_findings', []))} key findings\n")
            
            task4 = progress.add_task("[cyan]Generating report...", total=None)
            report = self.writer.write_report(query, summary)
            report_path = self._save_report(query, report)
            progress.update(task4, completed=True)
            self.console.print(f"[green]✓[/green] Report saved to: {report_path}\n")
            
            task5 = progress.add_task("[cyan]Updating memory systems...", total=None)
            self._update_memory(query, report, summary)
            progress.update(task5, completed=True)
            self.console.print("[green]✓[/green] Memory updated\n")
        
        self.knowledge_graph.end_session(session_id, "completed")
        
        return report_path
    
    def _execute_searches(self, subtasks):
        """Execute all search subtasks."""
        search_results = []
        
        for subtask in subtasks:
            if subtask.get("type") == "search":
                query = subtask.get("query", "")
                results = self.searcher.search(query)
                search_results.append(results)
        
        return search_results
    
    def _save_report(self, query: str, report: str) -> str:
        """Save the generated report to disk."""
        os.makedirs("storage/reports", exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = "".join(c if c.isalnum() else "_" for c in query)[:50]
        filename = f"report_{safe_query}_{timestamp}.md"
        filepath = os.path.join("storage/reports", filename)
        
        with open(filepath, 'w') as f:
            f.write(report)
        
        return filepath
    
    def _update_memory(self, query: str, report: str, summary: dict):
        """Store research results in memory systems."""
        self.vector_memory.store(
            text=query,
            metadata={
                "type": "research_query",
                "timestamp": datetime.now().isoformat(),
                "key_findings_count": len(summary.get("key_findings", [])),
                "source_count": summary.get("source_count", 0)
            }
        )
        
        for finding in summary.get("key_findings", [])[:5]:
            self.vector_memory.store(
                text=finding.get("point", ""),
                metadata={
                    "type": "key_finding",
                    "query": query,
                    "source": finding.get("source", "Unknown"),
                    "timestamp": datetime.now().isoformat()
                }
            )
    
    def show_stats(self):
        """Display system statistics."""
        self.console.print("\n[bold cyan]System Statistics[/bold cyan]")
        
        kg_stats = self.knowledge_graph.get_agent_stats()
        vm_stats = self.vector_memory.get_stats()
        
        stats_text = f"""
**Knowledge Graph:**
- Total Sessions: {kg_stats['total_sessions']}
- Total Actions: {kg_stats['total_actions']}
- Active Agents: {kg_stats['total_agents']}

**Vector Memory:**
- Stored Vectors: {vm_stats['total_vectors']}
- Embedding Dimension: {vm_stats['embedding_dimension']}
- Storage Size: {vm_stats['storage_size_kb']:.2f} KB
        """
        
        self.console.print(Panel(stats_text, border_style="cyan"))


def main():
    """Main entry point for the autonomous research agent."""
    agent = AutonomousResearchAgent()
    
    example_queries = [
        "2025 trends in open-source LLMs",
        "Latest developments in agentic AI systems",
        "Autonomous agents in real-world applications"
    ]
    
    print("\n" + "="*70)
    print("AUTONOMOUS RESEARCH AGENT - EDUCATIONAL DEMO")
    print("="*70)
    print("\nAvailable example queries:")
    for i, query in enumerate(example_queries, 1):
        print(f"{i}. {query}")
    print(f"{len(example_queries) + 1}. Custom query")
    print(f"{len(example_queries) + 2}. Show statistics")
    print("0. Exit")
    
    while True:
        try:
            choice = input(f"\nSelect option (0-{len(example_queries) + 2}): ").strip()
            
            if choice == "0":
                print("\nExiting. Thank you!")
                break
            elif choice == str(len(example_queries) + 1):
                query = input("\nEnter your research query: ").strip()
                if query:
                    report_path = agent.research(query)
                    print(f"\n✓ Research complete! Report saved to: {report_path}")
            elif choice == str(len(example_queries) + 2):
                agent.show_stats()
            elif choice.isdigit() and 1 <= int(choice) <= len(example_queries):
                query = example_queries[int(choice) - 1]
                report_path = agent.research(query)
                print(f"\n✓ Research complete! Report saved to: {report_path}")
            else:
                print("Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
