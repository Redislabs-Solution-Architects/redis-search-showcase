"""
embedding generation and management for movie plots
"""
import numpy as np
from sentence_transformers import SentenceTransformer
import struct

class MovieEmbeddings:
    """
    handles text embedding generation using sentence transformers
    """
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        initialize embedding model - using MiniLM for speed and quality
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
    
    def generate_embedding(self, text):
        """
        generate embedding vector from text
        """
        if not text:
            return None
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.astype(np.float32)
    
    def embedding_to_bytes(self, embedding):
        """
        convert numpy array to bytes for redis storage
        """
        if embedding is None:
            return None
        return struct.pack(f'{len(embedding)}f', *embedding)
    
    def bytes_to_embedding(self, bytes_data):
        """
        convert bytes back to numpy array
        """
        if not bytes_data:
            return None
        return np.array(struct.unpack(f'{len(bytes_data)//4}f', bytes_data))
    
    def cosine_similarity(self, vec1, vec2):
        """
        calculate cosine similarity between two vectors
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)