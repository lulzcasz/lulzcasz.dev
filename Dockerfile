FROM ghcr.io/astral-sh/uv:0.9-trixie AS web_development

WORKDIR /app

COPY . .

RUN uv sync

FROM ghcr.io/astral-sh/uv:0.9-trixie AS worker_development

WORKDIR /app

COPY . .

RUN apt update \ 
    && apt install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN uv sync

FROM ghcr.io/astral-sh/uv:0.9-trixie AS web_production

WORKDIR /app

COPY . .

RUN uv sync

CMD ["/bin/sh", "-c", "uv run manage.py collectstatic --no-input && uv run --no-dev gunicorn laboratoriodolyc.wsgi:application --bind 0.0.0.0:8000 --workers 5"]
#CMD ["uv", "run", "--no-dev", "gunicorn", "laboratoriodolyc.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "5"]

FROM ghcr.io/astral-sh/uv:0.9-trixie AS worker_production

WORKDIR /app

COPY . .

RUN apt update \ 
    && apt install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN uv sync --no-dev

CMD ["uv", "run", "--no-dev", "celery", "-A", "laboratoriodolyc", "worker", "-c", "2", "--loglevel", "INFO"]
