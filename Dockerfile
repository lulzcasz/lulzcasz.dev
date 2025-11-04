FROM ghcr.io/astral-sh/uv:0.9-trixie

WORKDIR /app

COPY . .

RUN uv sync
