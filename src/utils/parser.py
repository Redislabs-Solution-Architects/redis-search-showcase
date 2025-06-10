"""
shared utilities for redis movie search
"""
import re


def parse_redis_command(cmd):
    """
    parse redis search command while preserving syntax like quotes and brackets
    
    handles:
    - quoted strings: "star wars"
    - range brackets: [2010 2020]
    - field syntax: @genre:{Action}
    
    returns list of parsed tokens
    """
    parts = []
    current_token = ""
    in_quotes = False
    in_brackets = False
    i = 0
    
    while i < len(cmd):
        char = cmd[i]
        
        # handle quotes
        if char == '"' and (i == 0 or cmd[i-1] != '\\'):
            in_quotes = not in_quotes
            current_token += char
        # handle brackets for ranges
        elif char == '[':
            in_brackets = True
            current_token += char
        elif char == ']':
            in_brackets = False
            current_token += char
        # handle spaces
        elif char == ' ' and not in_quotes and not in_brackets:
            if current_token:
                parts.append(current_token)
                current_token = ""
        else:
            current_token += char
        
        i += 1
    
    # add the last token
    if current_token:
        parts.append(current_token)
    
    # clean up parts - remove quotes if they're the only content
    cleaned_parts = []
    for part in parts:
        if part.startswith('"') and part.endswith('"') and len(part) > 1:
            cleaned_parts.append(part[1:-1])
        else:
            cleaned_parts.append(part)
    
    return cleaned_parts


def parse_semantic_filters(filter_text):
    """
    parse filter syntax from hybrid search queries
    
    examples:
    - genre:Action year>2010
    - rating>7.5 year<2000
    
    returns dict of filters or None
    """
    filters = {}
    parts = filter_text.split()
    
    for part in parts:
        if part.startswith("genre:"):
            filters['genre'] = part.split(":", 1)[1]
        elif part.startswith("year>"):
            filters['year_min'] = int(part[5:])
        elif part.startswith("year<"):
            filters['year_max'] = int(part[5:])
        elif part.startswith("rating>"):
            filters['rating_min'] = float(part[7:])
    
    return filters if filters else None


def extract_k_parameter(query):
    """
    extract k parameter from query and return clean query + k value
    
    examples:
    - "k:10 space movie" -> ("space movie", 10)
    - "movie about robots k:5" -> ("movie about robots", 5)
    """
    k_match = re.search(r'\bk:(\d+)\b', query)
    if k_match:
        k_value = int(k_match.group(1))
        clean_query = re.sub(r'\bk:\d+\b', '', query).strip()
        return clean_query, k_value
    return query, None


def format_search_command(parts, index_name):
    """
    format search command parts with proper index and return clause
    """
    # check if index is specified, if not add default
    if len(parts) >= 1 and not parts[0].startswith('idx:'):
        parts.insert(0, index_name)
    
    # add return clause to exclude binary fields if not present
    if "RETURN" not in [p.upper() for p in parts]:
        parts.extend(["RETURN", "5", "title", "plot", "genre", "release_year", "rating"])
    
    return parts