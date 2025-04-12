import pytest
from src.utils.ai_analyzer import ProcessAnalyzer

@pytest.fixture
def analyzer():
    """Create ProcessAnalyzer instance for testing"""
    return ProcessAnalyzer()

def test_process_recommendations(analyzer):
    """Test getting process recommendations"""
    process = "Invoice Processing"
    steps = ["Manual data entry", "Email approvals", "Payment processing"]
    industry = "Finance"
    
    result = analyzer.get_process_recommendations(process, steps, industry)
    
    assert isinstance(result, dict)
    assert 'recommendations' in result
    assert 'process_name' in result
    assert result['process_name'] == process

def test_automation_scoring(analyzer):
    """Test automation potential scoring"""
    process_details = {
        'name': 'Customer Onboarding',
        'description': 'Manual process of collecting and verifying customer information',
        'tools': ['Email', 'Excel'],
        'frequency': 'Daily'
    }
    
    score = analyzer.score_automation_potential(process_details)
    
    assert isinstance(score, float)
    assert 0 <= score <= 100