# Redis Movie Search

A Python application to download movie data and load it into Redis Cloud with search capabilities.

## What This Does

1. Loads movie and actor data into your Redis Cloud database
2. Creates RediSearch indexes for fast querying
3. Provides a command-line interface for search

## Prerequisites

- Python 3.8+
- Redis Cloud account with RediSearch module enabled

## Quick Start

### 1. Clone and Setup

```bash
cd redis-movie-search
pip3 install -r requirements.txt
```

### 2. Configure Redis Connection

Copy the example environment file and add your Redis Cloud credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Redis Cloud details:
```
REDIS_HOST=your-redis-cloud-endpoint.redis-cloud.com
REDIS_PORT=16379
REDIS_PASSWORD=your-redis-cloud-password
```

### 3. Run Setup

```bash
python3 src/main.py setup
```

This will show an interactive menu:
- **Option 1**: Full setup (load data + create indexes)
- **Option 2**: Load data only
- **Option 3**: Create indexes only
- **Option 4**: Exit

The setup will:
- Load ~2,200 movies and ~1,100 actors into Redis
- Create search indexes for fast querying

### 4. Search

```bash
python3 src/search.py
```

Then enter FT.SEARCH commands. See `SEARCH_EXAMPLES.md` for comprehensive examples.

## How It Works

1. **Data Source**: Movie data from Redis's sample datasets (included in `data/` folder)
2. **Storage**: Data is stored as Redis Hashes (movie:* and actor:* keys)
3. **Indexing**: RediSearch creates full-text indexes on titles, plots, names, etc.
4. **Search**: Uses Redis Query Engine for fast text search

## Project Structure

```
redis-movie-search/
├── src/
│   ├── config.py         # Redis connection config
│   ├── load_data.py      # Loads data efficiently using redis-cli
│   ├── create_index.py   # Creates RediSearch indexes
│   ├── search.py         # Interactive CLI search interface
│   └── main.py          # Main orchestrator
├── data/                 # Movie dataset (Redis commands)
│   ├── import_movies.redis
│   └── import_actors.redis
├── requirements.txt      # Python dependencies
└── .env                 # Your Redis credentials
```
