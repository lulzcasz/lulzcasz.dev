FROM ghcr.io/astral-sh/uv:0.9-trixie AS development

WORKDIR /app

COPY . .

RUN uv sync

FROM ghcr.io/astral-sh/uv:0.9-trixie AS worker

WORKDIR /app

COPY . .

RUN apt update \ 
    && apt install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN uv sync
