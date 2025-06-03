from config import RedisConfig

def create_movie_index(client):
    """Create search index for movies"""
    index_name = "idx:movies"
    
    try:
        client.execute_command("FT.DROPINDEX", index_name)
    except:
        pass 
    
    try:
        client.execute_command(
            "FT.CREATE", index_name,
            "ON", "HASH",
            "PREFIX", "1", "movie:",
            "SCHEMA",
            "title", "TEXT", "WEIGHT", "5.0",
            "plot", "TEXT",
            "genre", "TAG",
            "release_year", "NUMERIC", "SORTABLE",
            "rating", "NUMERIC", "SORTABLE"
        )
        return True
    except Exception as e:
        print(f"Failed to create movie index: {e}")
        return False

def create_actor_index(client):
    """Create search index for actors"""
    index_name = "idx:actors"
    
    try:
        client.execute_command("FT.DROPINDEX", index_name)
    except:
        pass
    
    try:
        client.execute_command(
            "FT.CREATE", index_name,
            "ON", "HASH",
            "PREFIX", "1", "actor:",
            "SCHEMA",
            "first_name", "TEXT",
            "last_name", "TEXT",
            "date_of_birth", "NUMERIC", "SORTABLE",
        )
        return True
    except Exception as e:
        print(f"Failed to create actor index: {e}")
        return False

def index_exists(client, index_name):
    """Check if a RediSearch index exists"""
    try:
        client.execute_command("FT.INFO", index_name)
        return True
    except:
        return False

def list_indexes(client):
    """List all RediSearch indexes"""
    try:
        indexes = client.execute_command("FT._LIST")
        return indexes
    except:
        return []

def create_all_indexes():
    """Create all search indexes"""
    config = RedisConfig()
    client = config.get_client()
    
    if not create_movie_index(client):
        return False
    
    if not create_actor_index(client):
        return False
    
    print("Indexes created successfully")
    return True

if __name__ == "__main__":
    create_all_indexes()