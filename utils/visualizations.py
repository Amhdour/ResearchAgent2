"""
Visualization Utility

Generates charts and visualizations for research reports.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any, Optional
from datetime import datetime
import os


class ReportVisualizer:
    """
    Creates visualizations for research reports.
    
    Features:
    - Source distribution charts
    - Credibility analysis graphs
    - Topic trend visualizations
    """
    
    def __init__(self, style='seaborn-v0_8-darkgrid'):
        """
        Initialize visualizer.
        
        Args:
            style: Matplotlib style
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        sns.set_palette("husl")
    
    def create_source_distribution_chart(
        self, 
        summary: Dict[str, Any], 
        output_path: Optional[str] = None
    ) -> str:
        """
        Create a chart showing source distribution.
        
        Args:
            summary: Research summary with sources
            output_path: Output file path
        
        Returns:
            Path to saved chart
        """
        sources = summary.get("sources", [])
        
        source_domains = {}
        for source in sources:
            url = source.get("url", "")
            try:
                domain = url.split("//")[1].split("/")[0]
                domain = domain.replace("www.", "")
                source_domains[domain] = source_domains.get(domain, 0) + 1
            except:
                source_domains["unknown"] = source_domains.get("unknown", 0) + 1
        
        if not source_domains:
            return ""
        
        sorted_sources = sorted(source_domains.items(), key=lambda x: x[1], reverse=True)[:10]
        domains, counts = zip(*sorted_sources) if sorted_sources else ([], [])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(domains, counts, color='steelblue')
        ax.set_xlabel('Number of Sources')
        ax.set_title('Source Distribution')
        ax.invert_yaxis()
        
        plt.tight_layout()
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"storage/reports/chart_sources_{timestamp}.png"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_credibility_chart(
        self, 
        summary: Dict[str, Any], 
        output_path: Optional[str] = None
    ) -> str:
        """
        Create a chart showing source credibility distribution.
        
        Args:
            summary: Research summary with credibility data
            output_path: Output file path
        
        Returns:
            Path to saved chart
        """
        key_findings = summary.get("key_findings", [])
        
        credibility_counts = {"high": 0, "medium": 0, "low": 0, "unknown": 0}
        for finding in key_findings:
            credibility = finding.get("credibility", "unknown").lower()
            credibility_counts[credibility] = credibility_counts.get(credibility, 0) + 1
        
        labels = [k.capitalize() for k, v in credibility_counts.items() if v > 0]
        sizes = [v for v in credibility_counts.values() if v > 0]
        colors = ['#2ecc71', '#f39c12', '#e74c3c', '#95a5a6'][:len(labels)]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('Source Credibility Distribution')
        
        plt.tight_layout()
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"storage/reports/chart_credibility_{timestamp}.png"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def create_theme_analysis_chart(
        self, 
        summary: Dict[str, Any], 
        output_path: Optional[str] = None
    ) -> str:
        """
        Create a chart showing identified themes.
        
        Args:
            summary: Research summary with themes
            output_path: Output file path
        
        Returns:
            Path to saved chart
        """
        themes = summary.get("themes", [])
        
        if not themes:
            return ""
        
        theme_counts = {theme: 1 for theme in themes}
        
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        theme_names, counts = zip(*sorted_themes) if sorted_themes else ([], [])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(range(len(theme_names)), counts, color='coral')
        ax.set_xticks(range(len(theme_names)))
        ax.set_xticklabels(theme_names, rotation=45, ha='right')
        ax.set_ylabel('Mentions')
        ax.set_title('Key Themes Identified')
        
        plt.tight_layout()
        
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"storage/reports/chart_themes_{timestamp}.png"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return output_path


def generate_all_visualizations(summary: Dict[str, Any], query: str) -> List[str]:
    """
    Generate all available visualizations for a research summary.
    
    Args:
        summary: Research summary data
        query: Research query
    
    Returns:
        List of paths to generated charts
    """
    visualizer = ReportVisualizer()
    charts = []
    
    try:
        chart_path = visualizer.create_source_distribution_chart(summary)
        if chart_path:
            charts.append(chart_path)
    except Exception as e:
        print(f"Failed to create source distribution chart: {e}")
    
    if summary.get("synthesis_method") == "llm":
        try:
            chart_path = visualizer.create_credibility_chart(summary)
            if chart_path:
                charts.append(chart_path)
        except Exception as e:
            print(f"Failed to create credibility chart: {e}")
        
        try:
            chart_path = visualizer.create_theme_analysis_chart(summary)
            if chart_path:
                charts.append(chart_path)
        except Exception as e:
            print(f"Failed to create theme chart: {e}")
    
    return charts
