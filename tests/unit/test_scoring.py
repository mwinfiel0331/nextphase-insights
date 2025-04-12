from src.utils.scoring import calculate_optimization_score

def test_optimization_score():
    """Test optimization score calculation"""
    test_client = {
        'manual_processes': 5,
        'tool_selections': {
            'automation': ['tool1', 'tool2'],
            'integration': ['tool3']
        },
        'progress': 75
    }
    
    score = calculate_optimization_score(test_client)
    assert 0 <= score <= 100
    
    # Test empty client
    empty_score = calculate_optimization_score({})
    assert empty_score == 0