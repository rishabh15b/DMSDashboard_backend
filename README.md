# DMS Dashboard Backend

A FastAPI-based backend for the Document Management System (DMS) Dashboard.

## Features

- **Document Management**: CRUD operations for documents with categories (Client PO, Vendor PO, Client Invoice, Vendor Invoice, Service Agreement)
- **Exception Tracking**: Manage document validation exceptions with severity levels
- **Alert System**: Real-time alerts for document issues and expirations
- **Dashboard Analytics**: KPIs, utilization trends, and category breakdowns
- **Chat Assistant**: AI-powered chat for document queries
- **File Upload**: Handle document uploads with validation
- **RESTful API**: Complete REST API with proper error handling

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database (easily configurable for PostgreSQL/MySQL)
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running the application

## Installation

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database and seed data**:
   ```bash
   python scripts/seed_data.py
   ```

## Running the Application

### Development Mode
```bash
python start.py
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## API Endpoints

### Dashboard
- `GET /api/dashboard` - Get dashboard insights and KPIs

### Documents
- `GET /api/documents` - List all documents
- `GET /api/documents/{id}` - Get document details with related exceptions/alerts
- `POST /api/documents` - Create new document
- `PUT /api/documents/{id}` - Update document
- `DELETE /api/documents/{id}` - Delete document

### Exceptions
- `GET /api/exceptions` - List all exceptions
- `GET /api/exceptions/{id}` - Get exception details
- `POST /api/exceptions` - Create new exception
- `PUT /api/exceptions/{id}` - Update exception
- `DELETE /api/exceptions/{id}` - Delete exception

### Alerts
- `GET /api/alerts` - List all alerts
- `GET /api/alerts/{id}` - Get alert details
- `POST /api/alerts` - Create new alert
- `PUT /api/alerts/{id}` - Update alert
- `DELETE /api/alerts/{id}` - Delete alert

### Chat
- `POST /api/chat` - Send message to AI assistant

### File Upload
- `POST /api/uploads` - Upload files
- `GET /api/uploads/{filename}` - Download file
- `DELETE /api/uploads/{filename}` - Delete file

## Configuration

Edit the `.env` file to configure:

- **Database**: SQLite by default, easily configurable for PostgreSQL/MySQL
- **Security**: JWT secret key and token expiration
- **OpenAI**: API key for enhanced chat functionality
- **File Upload**: Upload directory and file size limits
- **CORS**: Allowed origins for frontend integration

## Database Schema

### Documents
- Document metadata (title, category, client, vendor, amount, status)
- Processing information (confidence, linked documents)
- File storage (PDF URLs, file paths)

### Exceptions
- Document validation issues
- Severity levels (low, medium, high)
- Assignment and resolution tracking

### Alerts
- System notifications
- Alert levels (info, warning, critical)
- Document associations

## Development

### Adding New Features
1. Create models in `app/models.py`
2. Add schemas in `app/schemas.py`
3. Implement services in `app/services/`
4. Create routers in `app/routers/`
5. Update main app to include new routers

### Database Migrations
The application uses SQLAlchemy with automatic table creation. For production, consider using Alembic for proper migrations.

## Frontend Integration

The backend is designed to work seamlessly with the Next.js frontend. Set the `NEXT_PUBLIC_API_BASE_URL` environment variable in your frontend to point to this backend.

Example frontend configuration:
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Production Deployment

For production deployment:

1. **Use a production database** (PostgreSQL recommended)
2. **Set secure environment variables**
3. **Use a production ASGI server** (Gunicorn with Uvicorn workers)
4. **Set up proper logging and monitoring**
5. **Configure reverse proxy** (Nginx)

Example production command:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
