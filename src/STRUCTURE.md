# Source Code Structure

## Directory Organization

```
src/
├── __init__.py
├── main.py              # CLI entry point
├── core/                # Core infrastructure
│   ├── __init__.py
│   ├── config.py        # Redis connection configuration
│   ├── embeddings.py    # Text embedding generation (384-dim vectors)
│   └── indexes.py       # Redis index schema definitions
├── data/                # Data operations
│   ├── __init__.py
│   ├── indexer.py       # Creates Redis search indexes
│   └── loader.py        # Loads movie/actor data, generates embeddings
├── search/              # Search implementations
│   ├── __init__.py
│   ├── traditional.py   # Traditional Redis FT.SEARCH queries
│   ├── semantic.py      # Natural language search interface
│   └── vector.py        # Vector similarity search engine
└── utils/               # Utilities
    ├── __init__.py
    ├── display.py       # Result formatting and help text
    └── parser.py        # Query parsing utilities
```

## Module Descriptions

### Core Infrastructure (`core/`)
- **config.py**: Manages Redis connections with environment variables
- **embeddings.py**: Handles text-to-vector conversion using Sentence Transformers
- **indexes.py**: Defines search index schemas (movies, actors, vectors)

### Data Operations (`data/`)
- **loader.py**: Imports data from Redis command files, generates embeddings
- **indexer.py**: Creates and manages Redis search indexes

### Search Implementations (`search/`)
- **traditional.py**: Database-style queries (`@genre:{Action}`)
- **semantic.py**: Natural language interface (`space adventure`)
- **vector.py**: Core vector search with KNN and hybrid capabilities

### Utilities (`utils/`)
- **display.py**: Formats search results and shows help
- **parser.py**: Parses queries and extracts filters

## Key Design Decisions

1. **Separation of Concerns**: Each directory has a clear, single purpose
2. **Dependency Hierarchy**: Core modules have no internal dependencies
3. **Intuitive Imports**: `from src.core.config import RedisConfig`
4. **Scalability**: Easy to add new search types or utilities
5. **Testability**: Clear boundaries between modules

## Import Examples

```python
# From main.py
from src.core.config import RedisConfig
from src.data.loader import load_all_data
from src.search.semantic import run_semantic_search

# From search modules
from src.core.embeddings import MovieEmbeddings
from src.utils.display import display_semantic_results
```