"""
display formatting for search results
"""
import click


def display_traditional_results(results):
    """
    display results from traditional redis search
    
    format:
    - total count
    - each result with key and fields
    """
    total_results = results[0]
    click.echo(f"\nFound {total_results} results")
    
    if total_results > 0:
        # process results
        for i in range(1, len(results), 2):
            if i + 1 < len(results):
                key = results[i]
                fields = results[i + 1]
                
                click.echo(f"\n{'=' * 60}")
                click.echo(f"Key: {key}")
                click.echo(f"{'=' * 60}")
                
                # display fields
                for j in range(0, len(fields), 2):
                    if j + 1 < len(fields):
                        field_name = fields[j]
                        field_value = fields[j + 1]
                        
                        # truncate long values
                        if len(str(field_value)) > 100:
                            click.echo(f"{field_name}: {str(field_value)[:100]}...")
                        else:
                            click.echo(f"{field_name}: {field_value}")


def display_semantic_results(results, query):
    """
    display results from semantic vector search
    
    includes similarity scores and distance metrics
    """
    click.echo(f"\nSemantic search for: '{query}'")
    click.echo(f"Found {len(results)} results")
    
    for key, score, data in results:
        # decode key if it's bytes
        if isinstance(key, bytes):
            key = key.decode('utf-8')
            
        click.echo(f"\n{'=' * 60}")
        click.echo(f"Key: {key}")
        
        # convert distance to similarity for better understanding
        similarity = 1.0 - score if score <= 1.0 else 0.0
        click.echo(f"Distance: {score:.3f} (Similarity: {similarity:.1%})")
        click.echo(f"{'=' * 60}")
        
        # display fields
        for field_name, field_value in data.items():
            # decode field names and values if they're bytes
            if isinstance(field_name, bytes):
                field_name = field_name.decode('utf-8')
            if isinstance(field_value, bytes):
                field_value = field_value.decode('utf-8')
                
            if field_name != 'score':  # skip the score field as we show it above
                if len(str(field_value)) > 100:
                    click.echo(f"{field_name}: {str(field_value)[:100]}...")
                else:
                    click.echo(f"{field_name}: {field_value}")



def show_semantic_help(default_k=5):
    """
    display help for semantic-only interface
    """
    click.echo("\nVECTOR SEARCH HELP")
    click.echo("-" * 40)
    
    click.echo("\nSEMANTIC SEARCH:")
    click.echo("  space adventure with aliens")
    click.echo("  romantic comedy in Paris")
    
    click.echo("\nHYBRID SEARCH (vector + filters):")
    click.echo("  superhero movie | genre:Action year>2010")
    click.echo("  comedy | rating>7.5 year>2015")
    
    click.echo("\nSIMILAR MOVIES:")
    click.echo("  similar to movie:1")
    
    click.echo("\nRESULT COUNT:")
    click.echo(f"  k:10 <query>  (default: {default_k})")
    
    click.echo("\nFILTERS:")
    click.echo("  genre:Action, year>2010, rating>7.5")
    
    click.echo("\nCOMMANDS:")
    click.echo("  help, quit")