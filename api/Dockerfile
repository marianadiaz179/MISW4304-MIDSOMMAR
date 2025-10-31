FROM python:3.9-slim

# Prevent Python writing .pyc and enabling output flushing
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

# System deps (for psycopg2 etc.), then clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Use Pipenv but keep the venv inside the container
RUN pip install --no-cache-dir pipenv && \
    PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --ignore-pipfile && \
    # Ensure gunicorn is present (if not already in Pipfile.lock)
    PIPENV_VENV_IN_PROJECT=1 pipenv run pip install --no-cache-dir gunicorn

# Tell Flask/Gunicorn where the app is (adjust if you use an app factory)
# Example for a module-level `app` inside src/app.py -> import path `src.app:app`
ENV APP_IMPORT="src.app:app"
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_HOST=database-1.cn4u2kgsmb84.us-east-2.rds.amazonaws.com
ENV DB_PORT=5432
ENV DB_NAME=postgres
ENV SECRET_TOKEN=secretoken
ENV FLASK_ENV=production

# EB injects PORT (commonly 5000). We honor that.
EXPOSE 5000

# Run a real WSGI server and bind to 0.0.0.0:$PORT
CMD ["sh","-c","exec pipenv run gunicorn ${APP_IMPORT} --bind 0.0.0.0:${PORT:-5000} --workers ${WORKERS:-2} --threads ${THREADS:-2} --timeout ${TIMEOUT:-60}"]
