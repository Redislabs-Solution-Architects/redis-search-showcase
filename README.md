# Redis Query Engine Demo

**Two Complementary Search Approaches: Traditional + Vector**
Demonstrate Redis's versatility as both a traditional and vector DB.

## Two Demo Flows

### Flow 1: Traditional Search Demo **Keyword syntax** 
- Setup: Movies + RediSearch indexes
- Capabilities: Field matching, ranges, sorting
- Example: `@genre:{Action} @rating:[8 +inf]`
- **Value**: Redis as a powerful search database

### Flow 2: Vector Search Demo  
**Embedding-based semantic search** - Natural language with HNSW vectors  
- Setup: Movies + embeddings + vector index
- Capabilities: Semantic + Hybrid search
- Examples:
  - Semantic: `space adventure with aliens`
  - Hybrid: `superhero movie | genre:Action year>2010`
- **Value**: Redis with vector semantic search!


## Code Structure
- `src/core/` - Redis config, embeddings, index schemas  
- `src/data/` - Data loading and index creation
- `src/search/` - Traditional, semantic, and vector search
- `src/utils/` - As the name implies

## Quick Start

### 1. Setup
```bash
git clone <repo>
cd redis-movie-search
pip3 install -r requirements.txt

# Configure Redis connection
cp .env.example .env
# Edit .env with your Redis credentials
```

### 2. Choose Your Demo Flow
```bash
python3 run.py setup
```

### 3. Run the Demo
```bash
# Flow 1: Database syntax
python3 run.py search-basic

# Flow 2: Natural language  
python3 run.py search-advanced
```

## Examples

### Keyword Search (Flow 1)
Traditional keyword syntax with precise field matching:
```bash
@genre:{Action} @rating:[8 +inf]
@title:star wars
@release_year:[2010 2020] SORTBY rating DESC
@genre:{Comedy} @rating:[7 10] LIMIT 0 5
```

### Hybrid Search (Flow 2)  
Embedding-based semantic search with natural language queries:

**Semantic (vector similarity):**  
```bash
space adventure with aliens
romantic comedy in Paris
movies about time travel
psychological thriller
```

**Hybrid (vector + traditional filters):**
```bash
superhero movie | genre:Action year>2010
comedy | rating>7.5 year>2015
space adventure | year<2000
```

## Requirements

- Python 3.8+
- Redis Stack (RediSearch + Vector support)
- 1GB RAM for embeddings