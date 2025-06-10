import click
from src.core.config import RedisConfig
from src.core.embeddings import MovieEmbeddings
from src.core.indexes import MOVIE_INDEX, MOVIE_VECTOR_INDEX, ACTOR_INDEX

def create_movie_index(client):
    """Create search index for movies with text and numeric fields"""
    index_config = MOVIE_INDEX
    index_name = index_config["name"]
    
    _drop_index_if_exists(client, index_name)
    
    try:
        # Build command from index configuration
        cmd = ["FT.CREATE", index_name, "ON", index_config["on"]]
        
        # Add prefix
        cmd.extend(["PREFIX", str(len(index_config["prefix"]))])
        cmd.extend(index_config["prefix"])
        
        # Add schema
        cmd.append("SCHEMA")
        for field_def in index_config["schema"]:
            cmd.extend(field_def)
        
        client.execute_command(*cmd)
        return True
    except Exception as e:
        click.echo(f"Failed to create movie index: {e}")
        return False

def create_actor_index(client):
    """Create search index for actors with name and birth date fields"""
    index_config = ACTOR_INDEX
    index_name = index_config["name"]
    
    _drop_index_if_exists(client, index_name)
    
    try:
        # Build command from index configuration
        cmd = ["FT.CREATE", index_name, "ON", index_config["on"]]
        
        # Add prefix
        cmd.extend(["PREFIX", str(len(index_config["prefix"]))])
        cmd.extend(index_config["prefix"])
        
        # Add schema
        cmd.append("SCHEMA")
        for field_def in index_config["schema"]:
            cmd.extend(field_def)
        
        client.execute_command(*cmd)
        return True
    except Exception as e:
        click.echo(f"Failed to create actor index: {e}")
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

def create_movie_index_with_vectors(client):
    """Create search index for movies with vector embedding support"""
    index_config = MOVIE_VECTOR_INDEX.copy()
    index_name = index_config["name"]
    embeddings = MovieEmbeddings()
    vector_dim = embeddings.dimension
    
    _drop_index_if_exists(client, index_name)
    
    try:
        # Build command from index configuration
        cmd = ["FT.CREATE", index_name, "ON", index_config["on"]]
        
        # Add prefix
        cmd.extend(["PREFIX", str(len(index_config["prefix"]))])
        cmd.extend(index_config["prefix"])
        
        # Add schema with dynamic vector dimension
        cmd.append("SCHEMA")
        for field_def in index_config["schema"]:
            # Replace dimension placeholder with actual value
            if isinstance(field_def, tuple):
                field_def = list(field_def)
                for i, val in enumerate(field_def):
                    if val == "384":  # Our dimension placeholder
                        field_def[i] = str(vector_dim)
            cmd.extend(field_def)
        
        client.execute_command(*cmd)
        click.echo(f"Created vector index '{index_name}' with {vector_dim}D vectors")
        return True
    except Exception as e:
        click.echo(f"Failed to create vector index: {e}")
        return False

def create_all_indexes(with_vectors=False):
    """Create all required search indexes"""
    config = RedisConfig()
    client = config.get_client()
    
    indexes_created = [
        ("movie", create_movie_index(client)),
        ("actor", create_actor_index(client))
    ]
    
    if with_vectors:
        vector_success = create_movie_index_with_vectors(client)
        indexes_created.append(("vector", vector_success))
        if not vector_success:
            click.echo("Warning: Vector index creation failed")
    
    success = all(result for _, result in indexes_created)
    
    if success:
        click.echo("All indexes created successfully")
    else:
        failed = [name for name, result in indexes_created if not result]
        click.echo(f"Failed to create indexes: {', '.join(failed)}")
    
    return success

def _drop_index_if_exists(client, index_name):
    """Drop index if it exists, ignore errors if it doesn't"""
    try:
        client.execute_command("FT.DROPINDEX", index_name)
    except:
        pass

if __name__ == "__main__":
    create_all_indexes()