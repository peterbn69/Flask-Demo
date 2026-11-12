FROM python:3.15-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_DEBUG=0

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN useradd --system --user-group app \
    && mkdir -p /app/instance \
    && chown app:app /app/instance

COPY --chown=app:app . .

USER app

EXPOSE 5000

CMD ["sh", "-c", "flask --app wsgi db upgrade && exec gunicorn --bind 0.0.0.0:5000 --access-logfile - wsgi:app"]
