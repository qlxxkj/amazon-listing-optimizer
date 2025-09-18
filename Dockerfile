FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# install playwright deps and browsers
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget ca-certificates libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxrandr2 libxdamage1 libgbm1 libpangocairo-1.0-0 libxcb1 libx11-6 libxext6 \
 && rm -rf /var/lib/apt/lists/*
RUN playwright install --with-deps
COPY . .
CMD ["python", "main.py"]