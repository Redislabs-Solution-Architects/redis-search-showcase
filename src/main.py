#!/usr/bin/env python3
import click
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import RedisConfig
from load_data import load_all_data
from create_index import create_all_indexes

@click.group()
def cli():
    """Redis Movie Search - A simple tool to load and search movie data in Redis Cloud"""
    pass

@cli.command()
def setup():
    """Interactive setup: load data to Redis and create indexes"""
   
    config = RedisConfig()
    if not config.test_connection():
        click.echo("Please configure your Redis connection in .env file")
        return
    
    click.echo("\nSetup Options:")
    click.echo("1. Full setup (load data + create indexes)")
    click.echo("2. Load data only")
    click.echo("3. Create indexes only")
    click.echo("4. Exit")
    
    choice = click.prompt("\nEnter your choice (1-4)", type=int)
    
    if choice == 1:
        if not create_all_indexes():
            click.echo("Failed to create indexes")
            return
            
        if not load_all_data():
            click.echo("Failed to load data")
            return
            
    elif choice == 2:
        if not load_all_data():
            click.echo("Failed to load data")
            return
            
    elif choice == 3:
        if not create_all_indexes():
            click.echo("Failed to create indexes")
            return
            
    elif choice == 4:
        return
    else:
        click.echo("Invalid choice")
        return
    
    click.echo("\nSetup complete. Run 'python3 src/search.py' to search.")


@cli.command()
def check_indexes():
    """Check existing search indexes"""
    from create_index import list_indexes, index_exists
    
    config = RedisConfig()
    client = config.get_client()
    
    indexes = list_indexes(client)
    if not indexes:
        click.echo("No indexes found")
        return
        
    click.echo(f"Found {len(indexes)} index(es):")
    for idx in indexes:
        click.echo(f"  {idx}")
        
    for idx_name in ["idx:movies", "idx:actors"]:
        if index_exists(client, idx_name):
            click.echo(f"{idx_name}: exists")
        else:
            click.echo(f"{idx_name}: missing")

if __name__ == "__main__":
    cli()