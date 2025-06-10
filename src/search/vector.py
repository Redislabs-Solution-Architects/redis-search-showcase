"""
vector search implementation for semantic movie search
"""
import numpy as np
import click

class VectorSearch:
    """
    handles vector-based semantic search operations
    """
    def __init__(self, client, embeddings_model):
        self.client = client
        self.embeddings_model = embeddings_model
        self.index_name = "idx:movies_vector"
    
    def semantic_search(self, query_text, k=5):
        """
        perform semantic search using vector similarity
        
        args:
            query_text: natural language query
            k: number of results
        
        returns:
            list of (movie_key, score, movie_data) tuples
        """
        # generate embedding for query
        query_embedding = self.embeddings_model.generate_embedding(query_text)
        if query_embedding is None:
            return []
        
        # convert to bytes for redis
        query_bytes = self.embeddings_model.embedding_to_bytes(query_embedding)
        
        # build KNN query
        knn_query = f"*=>[KNN {k} @plot_embedding $query_vec AS score]"
        
        try:
            # execute vector search
            results = self.client.execute_command(
                "FT.SEARCH", self.index_name,
                knn_query,
                "PARAMS", "2", "query_vec", query_bytes,
                "RETURN", "5", "title", "plot", "genre", "release_year", "score",
                "SORTBY", "score",
                "DIALECT", "2"
            )
            
            return self._parse_search_results(results)
            
        except Exception as e:
            click.echo(f"Vector search error: {e}")
            return []
    
    def hybrid_search(self, query_text, filters=None, k=5):
        """
        combine vector search with traditional filters
        
        args:
            query_text: natural language query
            filters: dict of filters (genre, year_min, etc)
            k: number of results
        
        returns:
            list of (movie_key, score, movie_data) tuples
        """
        # generate embedding
        query_embedding = self.embeddings_model.generate_embedding(query_text)
        if query_embedding is None:
            return []
        
        query_bytes = self.embeddings_model.embedding_to_bytes(query_embedding)
        
        # build filter clause
        filter_clause = self._build_filter_clause(filters)
        
        # combine filters with KNN
        if filter_clause:
            query = f"({filter_clause})=>[KNN {k} @plot_embedding $query_vec AS score]"
        else:
            query = f"*=>[KNN {k} @plot_embedding $query_vec AS score]"
        
        try:
            results = self.client.execute_command(
                "FT.SEARCH", self.index_name,
                query,
                "PARAMS", "2", "query_vec", query_bytes,
                "RETURN", "6", "title", "plot", "genre", "release_year", "rating", "score",
                "SORTBY", "score",
                "DIALECT", "2"
            )
            
            return self._parse_search_results(results)
            
        except Exception as e:
            click.echo(f"Hybrid search error: {e}")
            return []
    
    def find_similar_movies(self, movie_key, k=5):
        """
        find movies similar to a given movie
        
        args:
            movie_key: redis key of the movie
            k: number of similar movies
        
        returns:
            list of (movie_key, score, movie_data) tuples
        """
        # get the movie's plot
        movie_data = self.client.hgetall(movie_key)
        plot = movie_data.get('plot', '')
        
        if not plot:
            return []
        
        # use the plot as query, skip the movie itself
        return self.semantic_search(plot, k=k+1)[1:]

    def _parse_search_results(self, results):
        """
        parse redis search results into structured format
        """
        total = results[0]
        movies = []
        
        for i in range(1, len(results), 2):
            if i + 1 < len(results):
                movie_key = results[i]
                fields = results[i + 1]
                
                # convert fields list to dict
                movie_data = {}
                for j in range(0, len(fields), 2):
                    if j + 1 < len(fields):
                        field_name = fields[j]
                        field_value = fields[j + 1]
                        movie_data[field_name] = field_value
                
                # extract score from the data
                score_value = movie_data.get(b'score', b'0')
                if isinstance(score_value, bytes):
                    score_value = float(score_value.decode('utf-8'))
                else:
                    score_value = float(score_value)
                
                movies.append((movie_key, score_value, movie_data))
        
        return movies
    
    def _build_filter_clause(self, filters):
        """
        build redis filter clause from filter dict
        """
        if not filters:
            return ""
        
        filter_parts = []
        if 'genre' in filters:
            filter_parts.append(f"@genre:{{{filters['genre']}}}")
        if 'year_min' in filters:
            filter_parts.append(f"@release_year:[{filters['year_min']} +inf]")
        if 'year_max' in filters:
            filter_parts.append(f"@release_year:[-inf {filters['year_max']}]")
        if 'rating_min' in filters:
            filter_parts.append(f"@rating:[{filters['rating_min']} +inf]")
        
        return " ".join(filter_parts)