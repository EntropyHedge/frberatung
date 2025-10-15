# right
# 3.13 isn’t released yet – use the current stable 3.10 image
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

# OS deps
RUN apt-get update && \
        apt-get install -y --no-install-recommends build-essential libpq-dev && \
        apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Python deps
COPY pyproject.toml uv.lock ./
RUN pip install --upgrade pip uv && \
    uv pip install --system -e .
    
# project code
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "wsgi:app"]