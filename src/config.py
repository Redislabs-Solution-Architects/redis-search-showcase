import os
from dotenv import load_dotenv
import redis

load_dotenv()

class RedisConfig:
    """Configuration for Redis Cloud connection"""
    
    def __init__(self):
        self.host = os.getenv('REDIS_HOST', 'localhost')
        self.port = int(os.getenv('REDIS_PORT', 6379))
        self.password = os.getenv('REDIS_PASSWORD', '')
        self.decode_responses = True
        
    def get_client(self):
        """Get Redis client instance"""
        return redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=self.decode_responses
        )
        
    def test_connection(self):
        """Test Redis connection"""
        try:
            client = self.get_client()
            client.ping()
            return True
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")
            return False