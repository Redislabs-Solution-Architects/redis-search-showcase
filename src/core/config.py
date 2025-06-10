"""
redis connection configuration
"""
import os
from dotenv import load_dotenv
import redis

load_dotenv()

class RedisConfig:
    """
    redis connection configuration from environment variables
    """
    
    def __init__(self, decode_responses=False):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.password = os.getenv('REDIS_PASSWORD', '')
        self.decode_responses = decode_responses
        
    def get_client(self):
        """
        create redis client with configured settings
        """
        return redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=self.decode_responses
        )
        
    def test_connection(self):
        """
        test redis connection
        """
        try:
            client = self.get_client()
            client.ping()
            return True
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")
            return False