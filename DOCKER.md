# Docker Configuration

## Dockerfile

**Fixed for new app structure:**

1. **Correct module path**: `uvicorn app.main:app` (not `main:app`)
2. **Environment variables**: 
   - `PYTHONDONTWRITEBYTECODE=1` - Prevents .pyc files
   - `PYTHONUNBUFFERED=1` - Real-time logs
   - `PYTHONPATH=/app` - Ensures imports work
3. **Optimized caching**: Requirements copied first for better layer caching
4. **Selective copying**: Only copies necessary files (`app/`, `main.py`, `config.env*`)

## .dockerignore

**Comprehensive exclusions:**
- Tests, cache files, git files
- Environment files (will use env vars or mounted config)
- Documentation and IDE files
- Reduces image size significantly

## Build & Run

```bash
# Build image
docker build -t portfolio-backend .

# Run container
docker run -p 8000:8000 --env-file config.env portfolio-backend
```

## Environment Variables

Pass via:
- `--env-file config.env` 
- Or individual `-e` flags
- Or mounted secret in production
