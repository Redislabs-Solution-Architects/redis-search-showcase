import click
from config import RedisConfig

@click.command()
def search():
    """Search Redis using FT.SEARCH commands"""
    
    config = RedisConfig()
    client = config.get_client()
    
    # Test connection
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
            # For range queries, we need to preserve the brackets as part of the argument
            # Split on spaces but keep quoted strings and ranges together
            import re
            
            # First check if it starts with FT.SEARCH
            cmd = command.strip()
            if cmd.upper().startswith('FT.SEARCH'):
                cmd = cmd[9:].strip()  # Remove "FT.SEARCH"
            
            # Parse the query manually to handle Redis Search syntax
            parts = []
            current_token = ""
            in_quotes = False
            in_brackets = False
            i = 0
            
            while i < len(cmd):
                char = cmd[i]
                
                # Handle quotes
                if char == '"' and (i == 0 or cmd[i-1] != '\\'):
                    in_quotes = not in_quotes
                    current_token += char
                # Handle brackets for ranges
                elif char == '[':
                    in_brackets = True
                    current_token += char
                elif char == ']':
                    in_brackets = False
                    current_token += char
                # Handle spaces
                elif char == ' ' and not in_quotes and not in_brackets:
                    if current_token:
                        parts.append(current_token)
                        current_token = ""
                else:
                    current_token += char
                
                i += 1
            
            # Add the last token
            if current_token:
                parts.append(current_token)
            
            # Clean up parts - remove quotes if they're the only content
            cleaned_parts = []
            for part in parts:
                if part.startswith('"') and part.endswith('"') and len(part) > 1:
                    cleaned_parts.append(part[1:-1])
                else:
                    cleaned_parts.append(part)
            
            if len(cleaned_parts) < 2:
                click.echo("Invalid command. Example: idx:movies 'star wars'")
                continue
            
            # Execute the command
            results = client.execute_command("FT.SEARCH", *cleaned_parts)
            
            # Display results
            total_results = results[0]
            click.echo(f"\nFound {total_results} results")
            
            if total_results > 0:
                # Process results
                for i in range(1, len(results), 2):
                    if i + 1 < len(results):
                        key = results[i]
                        fields = results[i + 1]
                        
                        click.echo(f"\n{'=' * 60}")
                        click.echo(f"Key: {key}")
                        click.echo(f"{'=' * 60}")
                        
                        # Display fields
                        for j in range(0, len(fields), 2):
                            if j + 1 < len(fields):
                                field_name = fields[j]
                                field_value = fields[j + 1]
                                if len(str(field_value)) > 100:
                                    click.echo(f"{field_name}: {str(field_value)[:100]}...")
                                else:
                                    click.echo(f"{field_name}: {field_value}")
            
        except Exception as e:
            click.echo(f"\nError: {e}")

if __name__ == "__main__":
    search()