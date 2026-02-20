# ── ShopNxt Dockerfile ────────────────────────────────────────────────────────
# Owner : Surya | samsurya899@gmail.com
# Port  : 5000
# ──────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim

# FIX 1: Set UTF-8 locale explicitly.
#         python:3.12-slim ships with NO locale → gunicorn raises
#         UnicodeDecodeError when Python source or templates contain
#         any non-ASCII characters. This one line fixes it.
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5000

WORKDIR /app

# FIX 2: Install curl so the container health-check in ECS works.
#         python:3.12-slim does NOT include curl by default.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# FIX 3: Pin Werkzeug alongside Flask.
#         Flask 3.x requires Werkzeug 3.x. Without pinning, pip sometimes
#         resolves an incompatible version → ImportError at startup.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# FIX 4: Gunicorn flags tuned for Fargate 0.25 vCPU / 512 MB
#   --workers 2        : 2 sync workers is right for 0.25 vCPU
#   --timeout 120      : give slow cold-start requests time to finish
#   --access-logfile - : route access log to stdout → CloudWatch
#   --error-logfile  - : route error  log to stderr → CloudWatch
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app:app"]

