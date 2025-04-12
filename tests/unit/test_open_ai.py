import os
from dotenv import load_dotenv
from src.utils.ai_analyzer import ProcessAnalyzer
import pytest
from unittest.mock import Mock, patch
import openai

@pytest.fixture
def mock_openai():
    """Mock OpenAI API responses"""
    with patch('openai.OpenAI') as mock_client:
        # Mock successful completion with different responses
        def mock_create(**kwargs):
            if 'automation potential' in kwargs['messages'][0]['content'].lower():
                return Mock(choices=[Mock(message=Mock(content="75"))])
            return Mock(choices=[Mock(message=Mock(content="""
                {
                    "automation_opportunities": ["Document scanning", "Data extraction"],
                    "digital_tools": ["OCR software", "Workflow automation"],
                    "efficiency_improvements": ["Parallel processing", "Automated validation"],
                    "risk_mitigation": ["Data backup", "Audit trails"]
                }
            """))])
            
        mock_client.return_value.chat.completions.create.side_effect = mock_create
        yield mock_client

@pytest.fixture
def analyzer(mock_openai):
    """Create ProcessAnalyzer instance for testing"""
    return ProcessAnalyzer()

def test_openai_connection(analyzer, caplog):
    """Test OpenAI API connection with minimal usage"""
    assert analyzer is not None, "ProcessAnalyzer initialization failed"
    assert analyzer.client is not None, "OpenAI client initialization failed"

def test_process_recommendations(analyzer):
    """Test getting process recommendations"""
    result = analyzer.get_process_recommendations(
        process_name="Invoice Processing",
        current_steps=["Manual data entry", "Email approvals"],
        industry="Finance"
    )
    
    assert isinstance(result, dict)
    assert 'recommendations' in result
    assert 'process_name' in result
    assert result['process_name'] == "Invoice Processing"
    assert result['industry'] == "Finance"

def test_automation_scoring(analyzer):
    """Test automation potential scoring"""
    test_process = {
        'name': 'Test Process',
        'description': 'Simple test process',
        'tools': ['Email'],
        'frequency': 'Daily'
    }
    
    score = analyzer.score_automation_potential(test_process)
    assert isinstance(score, float)
    assert 0 <= score <= 100

@pytest.mark.parametrize("invalid_process", [
    {},
    {'name': None},
    {'name': '', 'description': ''},
])
def test_invalid_process_data(analyzer, invalid_process):
    """Test handling of invalid process data"""
    with pytest.raises(Exception):
        analyzer.score_automation_potential(invalid_process)

@pytest.mark.skip(reason="Only run when testing actual API connection")
def test_live_api_connection():
    """Test actual API connection (skipped by default)"""
    analyzer = ProcessAnalyzer()
    response = analyzer._test_connection()
    assert response is not None

if __name__ == "__main__":
    pytest.main([__file__, '-v'])