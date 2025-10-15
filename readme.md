# Flask Bootstrap Application

A modern Flask application bootstrap with authentication, security features, background tasks, and a responsive frontend built with Tailwind CSS.

## Features

- **Authentication**: Ghost CMS integration with whitelist-based access control
- **Security**: Content Security Policy, rate limiting, CSRF protection, secure headers
- **Modern Frontend**: Tailwind CSS 4.x with custom animations and responsive design
- **Background Tasks**: Celery integration with Redis broker and scheduled tasks
- **Database**: SQLAlchemy with PostgreSQL and connection pooling
- **Caching**: Redis-based caching and session storage
- **Interactive**: HTMX for seamless user interactions
- **Responsive**: Mobile-first design with collapsible navigation
- **Blueprints**: Modular architecture with separated concerns
- **Production Ready**: WSGI configuration, systemd services, logging

## Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL
- Redis
- Node.js (for Tailwind CSS)
- uv (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd flask_bootstrap
   ```

2. **Set up Python environment**
   ```bash
   uv sync
   source .venv/bin/activate  # or `uv run` for commands
   ```

3. **Install frontend dependencies**
   ```bash
   npm install
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create database
   createdb your_database_name
   
   # Initialize migrations
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Build frontend assets**
   ```bash
   npm run build
   # or for development with watch mode:
   npm run watch
   ```

7. **Start services**
   ```bash
   # Start Redis (Ubuntu/Debian)
   sudo systemctl start redis-server
   
   # Start Flask development server
   python run.py
   
   # In separate terminals, start Celery services:
   celery -A app.make_celery worker --loglevel=info
   celery -A app.make_celery beat --loglevel=info
   ```

## Configuration

### Environment Variables

Key environment variables (see `.env.example` for complete list):

```bash
# Flask
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# Ghost CMS (for authentication)
GHOST_API_URL=https://your-ghost-site.com/members/api/member
```

### Authentication Setup

1. **Configure Ghost CMS integration** in `.env`
2. **Add user UUIDs to whitelist**:
   ```python
   # app/blueprints/auth/whitelist.py
   accepted_ids = [
       "your-ghost-user-uuid-here",
       "another-user-uuid"
   ]
   ```

## Project Structure

```text
flask_bootstrap/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Flask extensions
│   ├── auth_utils.py        # Authentication utilities
│   ├── commands.py          # CLI commands
│   ├── blueprints/          # Application modules
│   │   ├── main/            # Main routes
│   │   ├── auth/            # Authentication
│   │   └── api/             # API endpoints
│   ├── static/              # Static assets
│   │   ├── css/             # Compiled CSS
│   │   ├── js/              # JavaScript files
│   │   └── src/             # Source files
│   └── templates/           # Jinja2 templates
│       ├── partials/        # Reusable components
│       └── error/           # Error pages
├── service_templates/       # Systemd service files
├── run.py                   # Development server
├── wsgi.py                  # Production WSGI
└── pyproject.toml           # Python dependencies
```

## Development

### Frontend Development

```bash
# Watch mode for CSS changes
npm run watch

# Build for production
npm run build
```

### Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migrations
flask db upgrade

# Downgrade
flask db downgrade
```

### Background Tasks

Celery tasks are configured in `app/config.py`. Example tasks run daily at scheduled times:

- Data updates at 1:00 AM, 2:00 AM, 3:00 AM
- Configurable via crontab expressions

## Deployment

### Systemd Services

Service templates are provided in `service_templates/`:

1. **Copy and configure services**:
   ```bash
   sudo cp service_templates/celery_server.txt /etc/systemd/system/celery.service
   sudo cp service_templates/celerybeat.txt /etc/systemd/system/celerybeat.service
   
   # Edit paths and user/group as needed
   sudo systemctl daemon-reload
   sudo systemctl enable celery celerybeat
   sudo systemctl start celery celerybeat
   ```

2. **Web server**: Use `wsgi.py` with Gunicorn, uWSGI, or similar

### Production Checklist

- [ ] Set `ENV=production` in environment
- [ ] Configure secure `SECRET_KEY`
- [ ] Set up SSL/HTTPS
- [ ] Configure database connection pooling
- [ ] Set up log rotation
- [ ] Configure monitoring
- [ ] Test Celery tasks
- [ ] Verify security headers

## API

### Authentication

- `GET /auth/check_login` - Verify Ghost authentication
- `GET /auth/profile` - User profile (protected)
- `POST /auth/logout` - Logout

### API Endpoints

- `GET /api/` - API status
- Protected routes require authentication

## Customization

### Adding New Features

1. **Create new blueprint**:
   ```python
   # app/blueprints/feature/__init__.py
   from flask import Blueprint
   feature_bp = Blueprint('feature', __name__)
   from . import routes
   ```

2. **Register blueprint** in `app/__init__.py`

3. **Add routes, models, templates** as needed

### Styling

- Modify `app/static/src/input.css` for custom styles
- Update `tailwind.config.js` for theme customization
- Use CSS custom properties in `:root` for consistent theming


## License

