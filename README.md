# FastAPI Boilerplate

Production-ready FastAPI boilerplate with user authentication, database integration, and AI agent data extraction capabilities.

## Features

✅ **User Authentication**
- Signup with email verification
- Login with JWT tokens
- Update password
- Delete user account
- Protected routes with authentication

✅ **Database**
- SQLAlchemy ORM
- SQLite (easily switchable to PostgreSQL/MySQL)
- User model with timestamps

✅ **Security**
- JWT token authentication
- Password hashing with bcrypt
- HTTP Bearer token security

✅ **AI Agent Integration**
- File upload handling
- Celery task queue
- Redis for caching
- Async job processing

✅ **Production Ready**
- Structured logging
- Exception handling
- Request/response middleware
- CORS support
- Docker support
- Environment configuration

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Authentication

#### Signup
```http
POST /api/users/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

#### Login
```http
POST /api/users/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** Same as signup

#### Get Current User
```http
GET /api/users/me
Authorization: Bearer YOUR_TOKEN_HERE
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2024-01-01T00:00:00"
}
```

#### Update Password
```http
PUT /api/users/update-password
Authorization: Bearer YOUR_TOKEN_HERE
Content-Type: application/json

{
  "old_password": "oldpassword123",
  "new_password": "newpassword123"
}
```

**Response:**
```json
{
  "message": "Password updated successfully",
  "success": true
}
```

#### Delete User
```http
DELETE /api/users/delete
Authorization: Bearer YOUR_TOKEN_HERE
```

**Response:**
```json
{
  "message": "User account deleted successfully",
  "success": true
}
```

### AI Agent

#### Start Agent
```http
POST /api/agent/start
Content-Type: multipart/form-data

file: [your file]
callback: {"url": "https://example.com/callback"}
jobid: "job-123"
extra: {"key": "value"}
```

## Project Structure

```
flask_boiler_plate/
├── main.py                 # Application entry point
├── database.py            # Database configuration
├── requirements.txt       # Python dependencies
├── db.sqlite             # SQLite database
│
├── api/
│   ├── api.py            # Agent API routes
│   ├── api_helper.py     # Helper functions
│   └── users.py          # User authentication routes
│
├── core/
│   ├── config.py         # Configuration
│   ├── logger.py         # Logging setup
│   ├── exception_handlers.py  # Error handling
│   ├── api_call.py       # HTTP client
│   │
│   ├── auth/             # 🔐 Authentication Module
│   │   ├── models.py     # User database model
│   │   ├── schemas.py    # Pydantic validation schemas
│   │   ├── security.py   # JWT & password utilities
│   │   └── __init__.py   # Auth exports
│   │
│   └── middlewares/
│       ├── middleware.py              # Middleware registration
│       ├── logging_middleware.py      # Request logging
│       └── response_formatter_middleware.py  # Response formatting
│
├── ai_agent/
│   ├── init_agent.py     # Agent initialization
│   └── service.py        # Agent service
│
└── celery_app.py         # Celery configuration
```

## Configuration

Configuration is done via environment variables or the `Config` class in `core/config.py`:

### Server
- `HOST`: Server host (default: `0.0.0.0`)
- `PORT`: Server port (default: `8000`)
- `DEBUG`: Debug mode (default: `true` in development)

### Database
- Uses SQLite by default (`db.sqlite`)
- Change `DATABASE_URL` in `database.py` for other databases

### Authentication
- `SECRET_KEY`: JWT secret key (change in `auth.py` for production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration (default: 30 minutes)

### Redis
- `REDIS_HOST`: Redis host (default: `localhost`)
- `REDIS_PORT`: Redis port (default: `6379`)
- `REDIS_DB`: Redis database (default: `1`)

### Logging
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `LOG_FILE`: Log file path (default: `app.log`)

## Security Notes

⚠️ **Before Production:**

1. **Change the SECRET_KEY** in `auth.py`
   ```python
   SECRET_KEY = "your-very-secure-random-key-here"
   ```

2. **Use environment variables** for sensitive data
   ```bash
   export SECRET_KEY="your-secret-key"
   export DATABASE_URL="postgresql://user:pass@localhost/db"
   ```

3. **Enable HTTPS** in production

4. **Use a production database** (PostgreSQL, MySQL)
   ```python
   DATABASE_URL = "postgresql://user:password@localhost/dbname"
   ```

5. **Set strong password policies**

6. **Enable rate limiting**

## Docker Support

```bash
# Build
docker-compose build

# Run
docker-compose up

# Run in background
docker-compose up -d
```

## Testing

Visit http://localhost:8000/docs and test all endpoints directly in the Swagger UI.

### Test User Flow:

1. **Signup**: Create a new user
2. **Copy Token**: Copy the `access_token` from response
3. **Authorize**: Click "Authorize" button, paste token
4. **Test Protected Routes**: Try `/api/users/me`, `/api/users/update-password`

## Adding New Endpoints

1. **Create a new router** in `api/` directory:
```python
from fastapi import APIRouter, Depends
from auth import get_current_user

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/")
async def get_items(user = Depends(get_current_user)):
    return {"items": []}
```

2. **Include router** in `main.py`:
```python
from api.your_router import router
app.include_router(router, prefix="/api")
```

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload

# Run Celery worker
celery -A celery_app worker --loglevel=info

# Run Redis (if needed)
redis-server
```

## Troubleshooting

### Database Errors
```bash
# Delete database and restart
rm db.sqlite
python main.py
```

### Port Already in Use
```bash
# Change port
export PORT=8001
python main.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## License

MIT License - Feel free to use this boilerplate for your projects!

## Support

For issues and questions, please open an issue on the repository.

---

**Happy Coding! 🚀**
