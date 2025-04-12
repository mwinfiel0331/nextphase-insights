def calculate_optimization_score(client):
    """
    Calculate an optimization score based on client data
    
    Args:
        client (dict): Client data dictionary
    Returns:
        float: Optimization score between 0-100
    """
    score = 0
    
    # Base score from manual processes
    if client.get('manual_processes'):
        score += max(0, 100 - (client['manual_processes'] * 10))
    
    # Tool adoption score
    if client.get('tool_selections'):
        tool_count = sum(len(tools) for tools in client['tool_selections'].values())
        score += min(50, tool_count * 5)
    
    # Progress score
    if client.get('progress', 0):
        score = (score + client['progress']) / 2
    
    return min(100, score)