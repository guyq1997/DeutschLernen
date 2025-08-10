# Database Setup Guide

## Local Development

For local development, the application will automatically create a SQLite database in the `data/words.db` file:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key_here

# Run the application (database will be created automatically)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The database file will be created at `./data/words.db` relative to the project root.

## Docker Development

For Docker development, the database will be mounted from your local `data` directory:

```bash
# Create local data directory if it doesn't exist
mkdir -p data

# Run with docker-compose (uses local ./data directory)
docker-compose up --build
```

The database will be persistent in your local `./data/words.db` file.

## Production Deployment

### Option 1: Mount Local Data Directory

Update the `docker-compose.prod.yml` file with your actual database path:

```yaml
volumes:
  - /path/to/your/local/database:/app/data
```

Then run:

```bash
# Copy your existing database to the target location
cp data/words.db /path/to/your/local/database/

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Direct Database File Mount

If you want to mount a specific database file:

```yaml
volumes:
  - /path/to/your/words.db:/app/data/words.db
  - /path/to/your/data:/app/data
```

## Database Migration

To migrate an existing database:

1. Stop the running container
2. Copy your `words.db` file to the mounted volume location
3. Restart the container

```bash
# Stop container
docker-compose down

# Copy database
cp /source/path/words.db ./data/

# Restart
docker-compose up -d
```

## Database Backup

To backup your database:

```bash
# Local development
cp data/words.db backup/words_$(date +%Y%m%d_%H%M%S).db

# Docker deployment
docker-compose exec deutsch-lernen cp /app/data/words.db /app/data/words_backup_$(date +%Y%m%d_%H%M%S).db
```

## Environment Variables

- `DOCKER_ENV=true` - Set this to use Docker paths for database location
- `OPENAI_API_KEY` - Required for AI features
- `PYTHONPATH=/app` - Set for proper Python module resolution