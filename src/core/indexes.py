"""
This file contains the index definitions used in the Redis Movie Search demo.
Each index showcases different Redis search capabilities
"""

# movie index for keyword search
MOVIE_INDEX = {
    "name": "idx:movies",
    "on": "HASH",
    "prefix": ["movie:"],
    "schema": [
        # Text field with boosted weight for title relevance
        ("title", "TEXT", "WEIGHT", "5.0"),
        
        # Text field for full-text search on plot descriptions
        ("plot", "TEXT"),
        
        # Tag field for exact matches on genres
        ("genre", "TAG"),
        
        # Numeric fields for range queries and sorting
        ("release_year", "NUMERIC", "SORTABLE"),
        ("rating", "NUMERIC", "SORTABLE")
    ]
}

# Vector index for semantic search with embeddings
MOVIE_VECTOR_INDEX = {
    "name": "idx:movies_vector",
    "on": "HASH", 
    "prefix": ["movie:"],
    "schema": [
        # Traditional search fields
        ("title", "TEXT", "WEIGHT", "5.0"),
        ("plot", "TEXT"),
        ("genre", "TAG"),
        ("release_year", "NUMERIC", "SORTABLE"),
        ("rating", "NUMERIC", "SORTABLE"),
        
        # Vector field for embeddings
        ("plot_embedding", "VECTOR", "HNSW", "6",
         "TYPE", "FLOAT32",
         "DIM", "384",
         "DISTANCE_METRIC", "COSINE")
    ]
}

# Actor index demonstrating multi-field search
ACTOR_INDEX = {
    "name": "idx:actors",
    "on": "HASH",
    "prefix": ["actor:"],
    "schema": [
        ("first_name", "TEXT"),
        ("last_name", "TEXT"),
        ("date_of_birth", "NUMERIC", "SORTABLE")
    ]
}
