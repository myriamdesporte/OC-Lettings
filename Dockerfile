# Image of the OC Lettings website, served by Gunicorn.

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first: this layer stays in cache while
# requirements.txt does not change, so rebuilds are faster.
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt

# Copy the project code (except the files listed in .dockerignore).
COPY . .

# Gather all static files in STATIC_ROOT, served by WhiteNoise.
# The secret key is only needed to load the settings: a throwaway value is used.
RUN DJANGO_SECRET_KEY=collectstatic-only python manage.py collectstatic --noinput

# Run the site as a non-root user.
# This user must be able to write the SQLite database (admin sessions).
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Port of the site inside the container (Render provides its own PORT variable).
ENV PORT=8000
EXPOSE 8000

# Production web server. Shell form so that ${PORT} is replaced at startup.
CMD ["sh", "-c", "exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT} --workers 2"]
