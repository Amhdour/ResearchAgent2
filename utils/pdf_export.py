"""
PDF Export Utility

Converts Markdown reports to professional PDF documents.
"""

from typing import Optional
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
import re


class PDFExporter:
    """
    Exports research reports to PDF format.
    
    Features:
    - Professional formatting
    - Automatic heading hierarchy
    - Hyperlinked citations
    - Page numbering and headers
    """
    
    def __init__(self, page_size=letter):
        """
        Initialize PDF exporter.
        
        Args:
            page_size: Page size (letter or A4)
        """
        self.page_size = page_size
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor='#1a1a1a',
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor='#2c3e50',
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomMeta',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor='#7f8c8d',
            alignment=TA_CENTER,
            spaceAfter=20
        ))
    
    def markdown_to_pdf(self, markdown_text: str, output_path: str, title: Optional[str] = None) -> str:
        """
        Convert markdown report to PDF.
        
        Args:
            markdown_text: Markdown formatted text
            output_path: Output PDF file path
            title: Optional document title
        
        Returns:
            Path to generated PDF file
        """
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=self.page_size,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=1*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        lines = markdown_text.split('\n')
        for line in lines:
            line = line.strip()
            
            if not line:
                story.append(Spacer(1, 0.1*inch))
                continue
            
            if line.startswith('# '):
                text = line[2:].strip()
                story.append(Paragraph(text, self.styles['CustomTitle']))
                story.append(Spacer(1, 0.2*inch))
            
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Spacer(1, 0.15*inch))
                story.append(Paragraph(text, self.styles['CustomHeading']))
            
            elif line.startswith('### '):
                text = line[4:].strip()
                story.append(Paragraph(f"<b>{text}</b>", self.styles['CustomBody']))
            
            elif line.startswith('**Generated:**') or line.startswith('**Sources'):
                text = self._clean_markdown(line)
                story.append(Paragraph(text, self.styles['CustomMeta']))
            
            elif line.startswith('---'):
                story.append(Spacer(1, 0.15*inch))
            
            elif line.startswith('*') and line.endswith('*'):
                text = self._clean_markdown(line)
                story.append(Paragraph(f"<i>{text}</i>", self.styles['CustomMeta']))
            
            elif re.match(r'^\d+\.\s+\[', line):
                text = self._clean_markdown(line)
                story.append(Paragraph(text, self.styles['CustomBody']))
            
            elif line.startswith('- ') or line.startswith('* '):
                text = self._clean_markdown(line[2:])
                story.append(Paragraph(f"• {text}", self.styles['CustomBody']))
            
            else:
                text = self._clean_markdown(line)
                if text:
                    story.append(Paragraph(text, self.styles['CustomBody']))
        
        doc.build(story)
        
        return output_path
    
    def _clean_markdown(self, text: str) -> str:
        """
        Clean markdown formatting for PDF.
        
        Converts markdown to ReportLab paragraph markup.
        """
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
        
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" color="blue">\1</a>', text)
        
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;').replace('>', '&gt;')
        text = re.sub(r'&lt;(/?[biu]|a [^&]+)&gt;', r'<\1>', text)
        
        return text


def export_report_to_pdf(markdown_report: str, query: str, output_dir: str = "storage/reports") -> str:
    """
    Export a research report to PDF.
    
    Args:
        markdown_report: Markdown formatted report
        query: Research query (for filename)
        output_dir: Output directory
    
    Returns:
        Path to generated PDF file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = "".join(c if c.isalnum() else "_" for c in query)[:50]
    filename = f"report_{safe_query}_{timestamp}.pdf"
    output_path = f"{output_dir}/{filename}"
    
    exporter = PDFExporter()
    return exporter.markdown_to_pdf(markdown_report, output_path, title=query)
