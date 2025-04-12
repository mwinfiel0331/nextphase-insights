import os
import time
from typing import List, Dict, Optional
import openai
from dotenv import load_dotenv
import logging
import json
import hashlib
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class ProcessAnalyzer:
    """AI-powered process analysis using OpenAI GPT"""
    
    def __init__(self):
        """Initialize OpenAI client with rate limiting"""
        self.client = openai.OpenAI()
        self.model = "gpt-3.5-turbo"
        self.retries = 1
        self.retry_delay = 5
    
    def _create_cache_key(self, *args, **kwargs) -> str:
        """Create a hashable cache key from arguments"""
        def make_hashable(obj):
            if isinstance(obj, (list, set)):
                return tuple(make_hashable(e) for e in obj)
            elif isinstance(obj, dict):
                return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
            return obj
        
        # Convert all arguments to hashable types
        hashable_args = tuple(make_hashable(arg) for arg in args)
        hashable_kwargs = {k: make_hashable(v) for k, v in kwargs.items()}
        
        # Create a unique string representation
        key_parts = [str(hashable_args), str(sorted(hashable_kwargs.items()))]
        return hashlib.md5(''.join(key_parts).encode()).hexdigest()

    def _make_api_request(self, messages: List[Dict], temperature: float, max_tokens: int) -> Dict:
        """Make actual API request"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return {'content': response.choices[0].message.content}
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    @lru_cache(maxsize=100)
    def _cached_api_request(self, cache_key: str, *, message_content: str, temperature: float, max_tokens: int) -> Dict:
        """Cached version of API request using hashable parameters"""
        messages = [{"role": "user", "content": message_content}]
        return self._make_api_request(messages, temperature, max_tokens)

    def get_process_recommendations(self, process_name: str, current_steps: List[str], industry: str) -> Dict:
        """Get AI-powered recommendations with caching"""
        try:
            message_content = f"""
            Analyze this business process and provide recommendations:
            Process: {process_name}
            Industry: {industry}
            Current Steps: {', '.join(current_steps)}
            """
            
            cache_key = self._create_cache_key(process_name, tuple(current_steps), industry)
            response = self._cached_api_request(
                cache_key,
                message_content=message_content,
                temperature=0.7,
                max_tokens=1000
            )
            
            return {
                'process_name': process_name,
                'industry': industry,
                'current_steps': current_steps,
                'recommendations': response['content'],
                'model_used': self.model
            }
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            raise

    def _validate_process(self, process_details: Dict) -> None:
        """Validate process details"""
        if not process_details:
            raise ValueError("Process details cannot be empty")
            
        name = process_details.get('name')
        if not name or not isinstance(name, str):
            raise ValueError("Process name must be a non-empty string")
            
        description = process_details.get('description', '').strip()
        if not description:
            raise ValueError("Process description cannot be empty")

    def score_automation_potential(self, process_details: Dict) -> float:
        """Calculate automation potential score using AI analysis"""
        try:
            self._validate_process(process_details)
            
            message_content = f"""
            Rate this process's automation potential (0-100):
            Process: {process_details['name']}
            Description: {process_details['description']}
            Tools: {', '.join(process_details.get('tools', []))}
            Frequency: {process_details.get('frequency', 'Unknown')}
            """
            
            cache_key = self._create_cache_key(
                process_details['name'],
                process_details['description'],
                tuple(process_details.get('tools', []))
            )
            
            response = self._cached_api_request(
                cache_key,
                message_content=message_content,
                temperature=0.3,
                max_tokens=50
            )
            
            return float(response['content'].strip())
        except Exception as e:
            logger.error(f"Error calculating automation score: {str(e)}")
            raise