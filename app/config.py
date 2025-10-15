import os
from dotenv import load_dotenv
from celery.schedules import crontab  # keep if you use beat
import redis

load_dotenv()


class BaseConfig:
    # ───────────────────────── General ─────────────────────────
    ENV: str = os.getenv("FLASK_ENV", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me")

    # ──────────────────────── PostgreSQL ───────────────────────
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_size": int(os.getenv("DB_POOL_SIZE", 15)),
        "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", 3600)),
        "pool_pre_ping": True,
        "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", 30)),
        "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", 25)),
        "connect_args": {
            "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", 15)),
            "sslmode": os.getenv("DB_SSLMODE", "disable"),
            "application_name": os.getenv("APP_NAME", "saas_app"),
        },
    }

    # ───────────────────────── Redis ───────────────────────────
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_URL: str = f"redis://{REDIS_HOST}:6379/0"

    # Flask-Caching
    CACHE_TYPE: str = "RedisCache"
    CACHE_REDIS_URL: str = REDIS_URL

    # Flask-Session
    SESSION_TYPE: str = "redis"
    SESSION_REDIS = redis.from_url(REDIS_URL)
    PERMANENT_SESSION_LIFETIME: int = 86_400
    SESSION_USE_SIGNER: bool = True

    # Celery
    broker_url: str = REDIS_URL
    result_backend: str = REDIS_URL
    CELERY = {
        "broker_url": broker_url,
        "result_backend": result_backend,
        "task_ignore_result": True,
        "beat_schedule": {},  # add crontab tasks here
    }

    # ─────────────────── Flask-Talisman defaults ───────────────
    TALISMAN_FORCE_HTTPS: bool = True
    TALISMAN_CSP: dict = {
        "default-src": ["'self'"],
        "img-src": ["'self'", "data:", "https:"],
        "font-src": ["'self'", "https:", "data:"],
    }


class ProductionConfig(BaseConfig):
    ENV = "production"
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # inherits TALISMAN_FORCE_HTTPS = True  → redirect to HTTPS


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SAMESITE = "Lax"
    TALISMAN_FORCE_HTTPS = False                       # ← no redirect
    TALISMAN_CSP = {
        **BaseConfig.TALISMAN_CSP,
        "script-src": [
            "'self'",
            "'unsafe-inline'",
            "https://cdn.tailwindcss.com",
            "https://cdnjs.cloudflare.com",
        ],
        "style-src": [
            "'self'",
            "'unsafe-inline'",
            "https://cdn.tailwindcss.com",
            "https://cdnjs.cloudflare.com",
            "https://fonts.googleapis.com"
        ],
    }
