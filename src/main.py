#!/usr/bin/env python3
"""
main entry point for redis movie search demos
"""
import click
import sys
from pathlib import Path

# add src directory to path
src_dir = Path(__file__).parent
sys.path.insert(0, str(src_dir))

# handle running from project root
if src_dir.name == 'src':
    project_root = src_dir.parent
    sys.path.insert(0, str(project_root / 'src'))

from src.core.config import RedisConfig
from src.data.indexer import create_all_indexes, create_movie_index_with_vectors
from src.data.loader import load_all_data, generate_embeddings_for_movies

@click.group()
def cli():
    """
    redis movie search - traditional and vector search demos
    """
    pass

@cli.command()
def setup():
    """
    setup redis with movie data and create search indexes
    """
    config = RedisConfig()
    if not config.test_connection():
        click.echo("Please configure your Redis connection in .env file")
        return
    
    _show_setup_options()
    choice = click.prompt("\nEnter your choice (1-4)", type=int)
    
    if choice == 1:
        _setup_advanced_demo()  # vector search
    elif choice == 2:
        _setup_basic_demo()     # traditional search
    elif choice == 3:
        _setup_upgrade()        # add vectors to existing data
    elif choice == 4:
        return
    else:
        click.echo("Invalid choice")

def _show_setup_options():
    """
    display setup menu options
    """
    click.echo("\nRedis Movie Search Setup")
    click.echo("-" * 30)
    click.echo("\n1. Vector Search Demo")
    click.echo("   Semantic + hybrid search with natural language")
    click.echo("   Example: 'space adventure', 'superhero | genre:Action'")
    click.echo("\n2. Traditional Search Demo")  
    click.echo("   Keyword syntax with inverted indexes")
    click.echo("   Example: '@genre:{Action} @rating:[8 +inf]'")
    click.echo("\n3. Upgrade existing data with vector search")
    click.echo("\n4. Exit")

def _setup_advanced_demo():
    """
    setup vector search with embeddings
    """
    click.echo("\nSetting up vector search demo...")
    
    if not create_all_indexes(with_vectors=True):
        click.echo("Failed to create indexes")
        return
        
    if not load_all_data():
        click.echo("Failed to load data")
        return
    
    click.echo("Generating embeddings for movie plots...")
    generate_embeddings_for_movies()
    
    click.echo("\nSetup complete. Run: python3 run.py search-advanced")
    click.echo("\nExamples:")
    click.echo("  space adventure with aliens")
    click.echo("  superhero movie | genre:Action year>2010")

def _setup_basic_demo():
    """
    setup traditional search without vectors
    """
    click.echo("\nSetting up traditional search demo...")
    
    if not create_all_indexes(with_vectors=False):
        click.echo("Failed to create indexes")
        return
        
    if not load_all_data():
        click.echo("Failed to load data")
        return
        
    click.echo("\nSetup complete. Run: python3 run.py search-basic")
    click.echo("\nExamples:")
    click.echo("  @genre:{Action} @rating:[8 +inf]")
    click.echo("  @title:star wars")

def _setup_upgrade():
    """
    add vector search to existing traditional setup
    """
    click.echo("\nUpgrading to vector search...")
    
    config = RedisConfig()
    client = config.get_client()
    
    if not create_movie_index_with_vectors(client):
        click.echo("Failed to create vector index")
        return
    
    click.echo("Generating embeddings...")
    generate_embeddings_for_movies()
    
    click.echo("\nUpgrade complete. Run: python3 run.py search-advanced")
    click.echo("\nNew capabilities:")
    click.echo("  space adventure with aliens")
    click.echo("  superhero movie | genre:Action year>2010")

@cli.command()
def search_basic():
    """
    traditional redis search with field syntax
    """
    from src.search.traditional import run_traditional_search
    run_traditional_search()

@cli.command()
def search_advanced():
    """
    natural language search with semantic understanding
    """
    from src.search.semantic import run_semantic_search
    run_semantic_search()

@cli.command()
def demo():
    """
    show demo guide for both search types
    """
    click.echo("\nRedis Movie Search Demo Guide")
    click.echo("=" * 40)
    
    click.echo("\n1. TRADITIONAL SEARCH (search_basic)")
    click.echo("   Database-style queries with field syntax:")
    click.echo("   @genre:{Action} @rating:[8 +inf]")
    click.echo("   @title:star wars")
    click.echo("   @release_year:[2010 2020] SORTBY rating DESC")
    
    click.echo("\n2. VECTOR SEARCH (search_advanced)")
    click.echo("   Natural language with semantic understanding:")
    click.echo("   space adventure with aliens")
    click.echo("   superhero movie | genre:Action year>2010")
    click.echo("   similar to movie:1")
    
    click.echo("\nRun 'python3 run.py setup' to get started!")

if __name__ == "__main__":
    cli()