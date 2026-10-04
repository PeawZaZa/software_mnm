# Dockerfile — Inventory System v2.0.1
# build:  docker build -t mini-inventory:v2.0.1 .
# run:    docker run -it --rm -v inventory-data:/app/data -v "$PWD/exports:/app/exports" mini-inventory:v2.0.1
FROM python:3.12-slim

WORKDIR /app

# ติดตั้ง dependencies ก่อนคัดลอกโค้ด เพื่อให้ Docker cache ชั้นนี้ไว้ได้
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_v2.py .

ENV INVENTORY_DB_PATH=/app/data/inventory_db.json \
    REPORT_EXPORT_DIR=/app/exports \
    PYTHONIOENCODING=utf-8

# ไม่รันด้วย root และแยกข้อมูลออกเป็น volume ให้อยู่รอดเมื่อลบ container
RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /app/data /app/exports \
    && chown -R appuser:appuser /app
USER appuser
VOLUME ["/app/data", "/app/exports"]

CMD ["python", "app_v2.py"]
