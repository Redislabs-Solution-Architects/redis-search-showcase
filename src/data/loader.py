import os
import subprocess
from src.core.config import RedisConfig
from src.core.embeddings import MovieEmbeddings
import click
import time

def load_all_data():
    """ load all movie and actor data into Redis from predefined files."""
    config = RedisConfig()
    
    if not config.test_connection():
        return False
    client = config.get_client()
    if _data_exists(client):
        return True
    
    redis_cli_cmd = _build_redis_cli_command(config)
    data_files = ["data/import_movies.redis", "data/import_actors.redis"]
    success = _load_data_files(data_files, redis_cli_cmd)
    if success:
        _display_load_statistics(client)
    
    return success

def _data_exists(client):
    """ check if data already exists in Redis"""
    for pattern in ["movie:*", "actor:*"]:
        for _ in client.scan_iter(match=pattern, count=1):
            click.echo("Data already exists - skipping load to avoid duplicates")
            return True
    return False

def _build_redis_cli_command(config):
    """ build redis-cli command with connection parameters"""
    cmd = ['redis-cli', '-h', config.host, '-p', str(config.port)]
    if config.password:
        cmd.extend(['-a', config.password])
    return cmd

def _load_data_files(data_files, redis_cli_cmd):
    """Load all data files using redis-cli"""
    for filepath in data_files:
        if not _load_single_file(filepath, redis_cli_cmd):
            return False
    return True

def _load_single_file(filepath, redis_cli_cmd):
    """Load a single data file into Redis"""
    if not os.path.exists(filepath):
        click.echo(f"File not found: {filepath}")
        return False
        
    filename = os.path.basename(filepath)
    click.echo(f"Loading {filename}...")
    
    try:
        with open(filepath, 'r') as f:
            result = subprocess.run(
                redis_cli_cmd,
                stdin=f,
                capture_output=True,
                text=True
            )
            
        if result.returncode == 0:
            click.echo(f"✓ {filename} loaded successfully")
            return True
        else:
            click.echo(f"✗ Error loading {filename}: {result.stderr}")
            return False
            
    except Exception as e:
        click.echo(f"✗ Failed to load {filename}: {e}")
        return False

def _display_load_statistics(client):
    """Display stats after successful data load"""
    movie_count = len(list(client.scan_iter(match="movie:*", count=100)))
    actor_count = len(list(client.scan_iter(match="actor:*", count=100)))
    click.echo(f"\n✓ Data load complete: {movie_count} movies, {actor_count} actors")

def generate_embeddings_for_movies(show_progress=True):
    """Generate vector embeddings for all movie plots"""
    config = RedisConfig(decode_responses=False)  # binary client for vectors
    client = config.get_client()
    text_client = RedisConfig(decode_responses=True).get_client()
    embeddings_model = MovieEmbeddings()
    
    movie_keys = _get_all_movie_keys(text_client)
    
    if show_progress:
        click.echo(f"\nFound {len(movie_keys)} movies to process")
    
    stats = _process_embeddings(movie_keys, text_client, client, embeddings_model, show_progress)
    
    if show_progress:
        _display_embedding_statistics(stats)
    
    return stats['processed'], stats['skipped'], stats['errors']

def _get_all_movie_keys(client):
    """Retrieve all movie keys from Redis"""
    movie_keys = []
    cursor = 0
    while True:
        cursor, keys = client.scan(cursor, match="movie:*", count=100)
        movie_keys.extend(keys)
        if cursor == 0:
            break
    return movie_keys

def _process_embeddings(movie_keys, text_client, binary_client, embeddings_model, show_progress):
    """Process embeddings for all movies with optional progress display"""
    stats = {'processed': 0, 'skipped': 0, 'errors': 0, 'start_time': time.time()}
    
    if show_progress:
        with click.progressbar(movie_keys, label='Processing movies') as bar:
            for key in bar:
                _update_embedding_stats(stats, text_client, binary_client, embeddings_model, key)
    else:
        for key in movie_keys:
            _update_embedding_stats(stats, text_client, binary_client, embeddings_model, key)
    
    return stats

def _update_embedding_stats(stats, text_client, binary_client, embeddings_model, key):
    """Update statistics based on embedding processing result"""
    success, skip, error = _process_movie_embedding(text_client, binary_client, embeddings_model, key)
    stats['processed'] += success
    stats['skipped'] += skip
    stats['errors'] += error

def _display_embedding_statistics(stats):
    """Display embedding generation statistics"""
    elapsed = time.time() - stats['start_time']
    rate = stats['processed'] / elapsed if elapsed > 0 else 0
    
    click.echo(f"\n✓ Embedding generation complete:")
    click.echo(f"  Processed: {stats['processed']} movies")
    click.echo(f"  Skipped: {stats['skipped']} (no plot)")
    click.echo(f"  Errors: {stats['errors']}")
    click.echo(f"  Time: {elapsed:.2f} seconds")
    click.echo(f"  Rate: {rate:.1f} movies/second")

def _process_movie_embedding(text_client, binary_client, embeddings_model, key):
    """Process embedding for a single movie - returns (success, skip, error)"""
    try:
        movie_data = text_client.hgetall(key)
        plot = movie_data.get('plot', '').strip()
        
        if not plot or plot == 'N/A':
            return 0, 1, 0  # Skip - no valid plot
        
        embedding = embeddings_model.generate_embedding(plot)
        if embedding is None:
            return 0, 1, 0  # Skip - embedding generation failed
        
        embedding_bytes = embeddings_model.embedding_to_bytes(embedding)
        binary_client.hset(key, 'plot_embedding', embedding_bytes)
        
        return 1, 0, 0  # Success
        
    except Exception:
        return 0, 0, 1  # Error

if __name__ == "__main__":
    load_all_data()