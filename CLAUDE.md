# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is "DeutschLernen" - a German vocabulary learning web application built with FastAPI and SQLite. The app helps users learn German vocabulary by tracking word mastery levels and providing AI-powered word extraction and text formatting features.

## Architecture

### Backend Structure
- **FastAPI Application**: Modern async Python web framework
- **SQLAlchemy ORM**: Database abstraction with SQLite backend
- **OpenAI Integration**: AI service for word generation and text formatting
- **Jinja2 Templates**: Server-side HTML rendering

### Key Components

1. **Database Layer** (`app/database.py`)
   - SQLite database with environment-based path configuration
   - Local development: `data/words.db`
   - Docker deployment: `/app/data/words.db` (mounted from host)
   - Session management with dependency injection pattern
   - Auto-creates data directory on startup

2. **Models** (`app/models.py`)
   - `Word` entity with fields: id, word, explanation, example, status, created_at
   - `LearningStatus` enum: NOT_MASTERED ("fremd"), MASTERED ("gemeistert"), NEED_TO_LEARN ("lernende")

3. **AI Service** (`app/ai_service.py`)
   - Word extraction from German text using GPT-4o-mini with structured output
   - Text formatting service using GPT-4o for better readability
   - Requires OPENAI_API_KEY environment variable

4. **Main Application** (`app/main.py`)
   - FastAPI routes for CRUD operations on words
   - Template rendering for web interface
   - JSON API endpoints for dynamic interactions

### Frontend Templates
- `base.html`: Base template with common layout
- `index.html`: Dashboard with word statistics
- `words.html`: Word list view
- `add_word.html`: Add new words form
- `words_card.html`: Study cards interface

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY=your_key_here

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Development
```bash
# Build and run with docker-compose (mounts local ./data directory)
docker-compose up --build

# Environment variables required in .env file:
# OPENAI_API_KEY=your_openai_key
```

### Production Deployment
```bash
# Update docker-compose.prod.yml with your database path
# Mount existing database: - /path/to/your/database:/app/data
docker-compose -f docker-compose.prod.yml up -d
```

### Database Operations
The database is automatically initialized on startup. To reset:
```python
from app.database import init_db
init_db()  # Drops and recreates all tables
```

## Key Features

1. **Word Management**: Add, edit, delete German words with explanations and examples
2. **Learning Status Tracking**: Three-tier mastery system (fremd/lernende/gemeistert)
3. **AI Word Extraction**: Extract and explain difficult German words from text passages
4. **Text Formatting**: AI-powered HTML formatting for better readability of German texts
5. **Study Interface**: Card-based learning system with status progression

## API Endpoints

- `GET /`: Dashboard with statistics
- `GET /words/{status}`: Filter words by learning status
- `POST /add_word`: Add multiple words from JSON
- `POST /update_status/{word_id}`: Update word learning status
- `POST /update_word/{word_id}`: Update word details
- `POST /generate_words`: AI extraction of words from text
- `POST /format_text`: AI formatting of German text
- `DELETE /delete_word/{word_id}`: Remove word

## Testing & Evaluation

The project includes a `promptfoo` configuration for testing AI prompt performance:
- Located in `prommptfoo/DeutschLernen/`
- Compares GPT-4o-mini vs GPT-4o for word extraction tasks
- Uses structured JSON output format validation

## Database Management

The application uses SQLite with automatic path detection:
- **Local Development**: Database stored in `./data/words.db`
- **Docker**: Database mounted from host at `/app/data/words.db`
- **Environment Variable**: Set `DOCKER_ENV=true` for Docker deployments

See `README_DATABASE.md` for detailed database setup, migration, and backup instructions.

## Environment Requirements

- Python 3.12+
- OpenAI API key for AI features
- SQLite (no additional database server needed)
- Docker support for containerized deployment
- Environment variables:
  - `OPENAI_API_KEY` - Required for AI features
  - `DOCKER_ENV=true` - Set for Docker deployments