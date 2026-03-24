# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/nonexistent" --shell "/sbin/nologin" --no-create-home --uid "${UID}" appuser

# Copy metadata
COPY pyproject.toml* setup.cfg* setup.py* README.md /app/

# Copy source
COPY src/ /app/src/

# Install package and dependencies
RUN python -m pip install --no-cache-dir .

# Ensure non-root can read app files
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["gunicorn", "--bind=0.0.0.0:8000", "scheduler_app.wsgi:app"]