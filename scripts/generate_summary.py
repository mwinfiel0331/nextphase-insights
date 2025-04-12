import click
from pathlib import Path
from src.utils.summary_generator import SummaryGenerator

@click.command()
@click.option('--current', prompt='Current state description', help='Description of current state')
@click.option('--changes', prompt='Proposed changes', help='Description of proposed changes')
def generate_summary(current: str, changes: str):
    """Generate a PDF summary of code changes"""
    try:
        generator = SummaryGenerator()
        output_file = generator.generate_summary(current, changes)
        click.echo(f"\n✅ Summary generated: {output_file}")
    except Exception as e:
        click.echo(f"\n❌ Error generating summary: {str(e)}")

if __name__ == "__main__":
    generate_summary()