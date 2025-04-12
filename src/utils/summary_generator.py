from fpdf import FPDF
from datetime import datetime
import openai
import os
from pathlib import Path

class SummaryGenerator:
    def __init__(self):
        self.pdf = FPDF()
        self.openai = openai
        self.openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def generate_summary(self, current_state: str, proposed_changes: str) -> Path:
        """Generate a PDF summary of current state and proposed changes"""
        try:
            # Get AI analysis
            analysis = self._get_ai_analysis(current_state, proposed_changes)
            
            # Create PDF
            self.pdf.add_page()
            self.pdf.set_font('Arial', 'B', 16)
            self.pdf.cell(0, 10, 'NextPhase Insights - Change Summary', ln=True, align='C')
            self.pdf.ln(10)
            
            # Add timestamp
            self.pdf.set_font('Arial', '', 10)
            self.pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
            
            # Add content sections
            self._add_section('Current State', current_state)
            self._add_section('Proposed Changes', proposed_changes)
            self._add_section('AI Analysis', analysis)
            
            # Save PDF
            output_dir = Path.cwd() / 'reports'
            output_dir.mkdir(exist_ok=True)
            
            filename = output_dir / f'change_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            self.pdf.output(str(filename))
            
            return filename
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            raise
    
    def _add_section(self, title: str, content: str):
        """Add a section to the PDF"""
        self.pdf.set_font('Arial', 'B', 12)
        self.pdf.cell(0, 10, title, ln=True)
        self.pdf.set_font('Arial', '', 10)
        self.pdf.multi_cell(0, 10, content)
        self.pdf.ln(10)
    
    def _get_ai_analysis(self, current_state: str, proposed_changes: str) -> str:
        """Get AI analysis of changes"""
        try:
            prompt = f"""
            Analyze the following code changes:
            
            Current State:
            {current_state}
            
            Proposed Changes:
            {proposed_changes}
            
            Provide a summary of:
            1. Key changes and their impact
            2. Potential risks or considerations
            3. Recommendations for testing
            """
            
            response = self.openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"