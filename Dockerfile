FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

RUN groupadd -g 1000 appuser && useradd -u 1000 -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY ./src ./src

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "src.app:app"]
