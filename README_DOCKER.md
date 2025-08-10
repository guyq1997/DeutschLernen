# DeutschLernen Docker Setup

This application now uses local persistent storage instead of AWS S3 for the SQLite database.

## Running with Docker Compose

```bash
# Build and start the application
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs deutsch-lernen

# Stop the application
docker-compose down
```

## Data Persistence

The SQLite database is stored in a Docker volume (`deutsch_lernen_data`) which persists data even when containers are recreated. The database file is located at `/app/data/words.db` within the container.

## Changes Made

- Removed AWS S3 backup functionality
- Updated database path to use persistent volume (`/app/data/words.db`)
- Removed boto3 dependency
- Added Docker Compose configuration with persistent volume mounting
- Simplified database initialization without S3 integration