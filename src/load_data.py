import os
import subprocess
from config import RedisConfig

def load_all_data():
    """Load movie data into Redis using redis-cli"""
    config = RedisConfig()
    
    if not config.test_connection():
        return False
    
    client = config.get_client()
    
    # Check if data already exists
    movie_count = 0
    actor_count = 0
    for key in client.scan_iter(match="movie:*", count=100):
        movie_count += 1
        break  # Just need to know if any exist
    for key in client.scan_iter(match="actor:*", count=100):
        actor_count += 1
        break  # Just need to know if any exist
        
    if movie_count > 0 or actor_count > 0:
        print(f"Data already exists in Redis")
        print("Skipping data load to avoid duplicates")
        return True
    
    print("Loading data...")
    
    # Build redis-cli command
    redis_cli_base = [
        'redis-cli',
        '-h', config.host,
        '-p', str(config.port),
    ]
    if config.password:
        redis_cli_base.extend(['-a', config.password])
    
    # Load data files
    data_files = [
        "data/import_movies.redis",
        "data/import_actors.redis"
    ]
    
    total_loaded = True
    
    for filepath in data_files:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return False
            
        filename = os.path.basename(filepath)
        print(f"Loading {filename}...")
        
        try:
            with open(filepath, 'r') as f:
                result = subprocess.run(
                    redis_cli_base,
                    stdin=f,
                    capture_output=True,
                    text=True
                )
                
            if result.returncode == 0:
                print("Loaded successfully")
            else:
                print(f"Error: {result.stderr}")
                total_loaded = False
                
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
            total_loaded = False
    
    if total_loaded:
        # Show statistics
        movie_count = len(list(client.scan_iter(match="movie:*", count=100)))
        actor_count = len(list(client.scan_iter(match="actor:*", count=100)))
        
        print(f"\nLoaded {movie_count} movies and {actor_count} actors")
    
    return total_loaded

if __name__ == "__main__":
    load_all_data()