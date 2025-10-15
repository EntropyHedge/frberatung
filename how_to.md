# FriedrichReport Setup Guide

This guide will walk you through setting up the FriedrichReport application from scratch. Follow these steps in order to ensure a proper setup.

## Prerequisites

### System Requirements
- Python 3.8+
- PostgreSQL 13+
- Node.js 16+
- Redis Server
- Git

## 1. Database Setup

### Install PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS (using Homebrew)
brew install postgresql
```

### Create Database
```bash
sudo -u postgres psql

# In PostgreSQL prompt
CREATE DATABASE friedrichreport;
CREATE USER friedrichuser WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE friedrichreport TO friedrichuser;
```

## 2. Redis Setup

### Install Redis
```bash
# Ubuntu/Debian
sudo apt install redis-server

# macOS
brew install redis
```

### Start Redis Service
```bash
# Ubuntu/Debian
sudo systemctl start redis-server
sudo systemctl enable redis-server

# macOS
brew services start redis
```

## 3. Python Environment Setup

### Create Virtual Environment
```bash
# Install uv if not already installed
pip install uv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
```

### Install Python Dependencies
```bash
uv sync
```

## 4. Frontend Dependencies

### Install Node.js and npm
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install nodejs

# macOS
brew install node
```

### Install Frontend Dependencies
```bash
npm install
```

## 5. Environment Configuration

Create a `.env` file in the project root:
```env
# Flask Configuration
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key_here

# Database Configuration
DATABASE_URL=postgresql://friedrichuser:your_password@localhost/friedrichreport

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Other Configurations
# Add any additional environment variables here
```

## 6. Initialize Database
```bash
# Create database tables
flask db upgrade

# Create admin user
flask create-user admin@example.com --admin
```

## 7. Celery Setup

### Start Celery Worker
```bash
# Start Celery worker
celery -A app.make_celery worker --loglevel INFO

# Start Celery beat (in a separate terminal)
celery -A app.make_celery beat --loglevel INFO
```

To run as services, create systemd service files (Linux):
```bash
sudo nano /etc/systemd/system/celery.service
sudo nano /etc/systemd/system/celerybeat.service
```

Then enable and start the services:
```bash
sudo systemctl enable celery celerybeat
sudo systemctl start celery celerybeat
```

## 8. Running the Application

### Development Mode
```bash
# Start the Flask development server
flask run

# In a separate terminal, start the frontend build process (if using TailwindCSS)
npm run watch
```

### Production Mode
For production deployment, use Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
```

## 9. Verify Installation

1. Visit `http://localhost:5000` in your browser
2. Log in with the admin credentials you created
3. Verify that the Celery tasks are running
4. Check Redis connection
5. Verify database connectivity

## Common Issues and Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in `.env`
- Ensure database exists: `psql -l`

### Redis Issues
- Verify Redis is running: `redis-cli ping`
- Check Redis connection in `.env`

### Celery Issues
- Verify Redis is running (required for Celery)
- Check Celery logs: `tail -f /var/log/celery/worker.log`
- Ensure Celery services are running: `sudo systemctl status celery`

## Security Notes

1. Change default passwords
2. Update SECRET_KEY in production
3. Configure proper firewall rules
4. Set up SSL/TLS in production
5. Regular security updates

## Maintenance

### Regular Maintenance Tasks
1. Database backups
2. Log rotation
3. System updates
4. Security patches

### Monitoring
1. Set up system monitoring
2. Configure error logging
3. Monitor disk space
4. Watch for system resource usage

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)

## Support

For issues and support:
1. Check the troubleshooting section above
2. Review project documentation
3. Submit an issue on GitHub
4. Contact the development team
