"""
semantic search interface for natural language queries
"""
import click
from src.core.config import RedisConfig
from src.core.embeddings import MovieEmbeddings
from src.search.vector import VectorSearch
from src.utils.parser import parse_semantic_filters, extract_k_parameter
from src.utils.display import display_semantic_results, show_semantic_help


def run_semantic_search():
    """
    run semantic search interface with natural language queries
    """
    # setup clients and models
    config = RedisConfig(decode_responses=False)  # binary client for vectors
    client = config.get_client()
    text_client = RedisConfig(decode_responses=True).get_client()
    
    # test connection
    try:
        client.ping()
    except Exception as e:
        click.echo(f"Failed to connect to Redis: {e}")
        return
    
    # initialize search components
    embeddings_model = MovieEmbeddings()
    vector_search = VectorSearch(client, embeddings_model)
    
    click.echo("\nVector-Based Redis Search (type 'quit' to exit, 'help' for options)")
    click.echo("Natural language queries with optional filters")
    
    while True:
        command = click.prompt('\nEnter natural language query', default='', show_default=False)
        
        if command.lower() == 'quit':
            click.echo("\nGoodbye!")
            break
            
        if command.lower() == 'help':
            show_semantic_help()
            continue
            
        if not command.strip():
            continue
        
        try:
            if command.lower().startswith('similar to '):
                # find similar movies
                movie_key = command[11:].strip()
                _find_similar_movies(movie_key, text_client, vector_search)
            else:
                # semantic or hybrid search
                _execute_semantic_search(command, vector_search)
                
        except Exception as e:
            click.echo(f"\nError: {e}")


def _execute_semantic_search(query, vector_search, default_k=5):
    """
    execute semantic search with optional filters
    """
    # extract k parameter if present
    clean_query, k_value = extract_k_parameter(query)
    num_results = k_value if k_value is not None else default_k
    
    # check for filters using | separator
    search_text = clean_query
    filters = None
    
    if " | " in clean_query:
        parts = clean_query.split(" | ", 1)
        search_text = parts[0].strip()
        filters = parse_semantic_filters(parts[1])
    
    # perform search
    if filters:
        results = vector_search.hybrid_search(search_text, filters, k=num_results)
    else:
        results = vector_search.semantic_search(search_text, k=num_results)
    
    # display results
    display_semantic_results(results, search_text)


def _find_similar_movies(movie_key, text_client, vector_search):
    """
    find movies similar to a given movie
    """
    # check if movie exists
    movie_data = text_client.hgetall(movie_key)
    if not movie_data:
        click.echo(f"Movie {movie_key} not found")
        return
    
    title = movie_data.get('title', 'Unknown')
    click.echo(f"\nFinding movies similar to: {title}")
    
    # find similar movies
    results = vector_search.find_similar_movies(movie_key, k=5)
    display_semantic_results(results, f"similar to {title}")


if __name__ == "__main__":
    run_semantic_search()