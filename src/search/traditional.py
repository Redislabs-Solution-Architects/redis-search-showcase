"""
traditional redis search with FT.SEARCH syntax
"""
import click
from src.core.config import RedisConfig
from src.utils.parser import parse_redis_command, format_search_command
from src.utils.display import display_traditional_results

def run_traditional_search():
    """
    run traditional redis search interface
    """
    config = RedisConfig(decode_responses=True)
    client = config.get_client()
    
    # test connection
    try:
        client.ping()
    except Exception as e:
        click.echo(f"Failed to connect to Redis: {e}")
        return
    
    click.echo("\nRedis Search (type 'quit' to exit)")
    click.echo("Format: FT.SEARCH index_name query [options]")
    click.echo("=" * 60)
    
    while True:
        command = click.prompt('\nEnter FT.SEARCH command', default='', show_default=False)
        
        if command.lower() == 'quit':
            click.echo("\nGoodbye!")
            break
            
        if not command.strip():
            continue
        
        try:
            # handle FT.SEARCH prefix
            cmd = command.strip()
            if cmd.upper().startswith('FT.SEARCH'):
                cmd = cmd[9:].strip()
            
            # parse command preserving redis syntax
            parts = parse_redis_command(cmd)
            
            if len(parts) < 2:
                click.echo("Invalid command. Example: idx:movies 'star wars' or just '@title:star wars'")
                continue
            
            # format with proper index and return clause
            parts = format_search_command(parts, 'idx:movies')
            
            # execute search
            results = client.execute_command("FT.SEARCH", *parts)
            
            # display results
            display_traditional_results(results)
            
        except Exception as e:
            click.echo(f"\nError: {e}")

if __name__ == "__main__":
    run_traditional_search()