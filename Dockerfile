FROM python:3.13-slim AS builder

WORKDIR /COCOB
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- PROD STAGE ----
FROM python:3.13-slim

# system deps (e.g., psycopg needs libpq)
RUN apt-get update && apt-get install -y --no-install-recommends curl libpq5 && rm -rf /var/lib/apt/lists/*

# non-root user
RUN useradd -m -r -d /COCOB cocouser

WORKDIR /COCOB

# copy deps
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# copy app
COPY . .

# static dir must be writable by app
RUN mkdir -p /COCOB/staticfiles && chown -R cocouser:cocouser /COCOB
USER cocouser

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

EXPOSE 8000

# ensure LF endings and executable
RUN chmod +x /COCOB/entrypoint.prod.sh

CMD ["/COCOB/entrypoint.prod.sh"]
