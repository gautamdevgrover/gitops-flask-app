FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Set default version (can be overridden by Jenkins)
ENV APP_VERSION=1

EXPOSE 5000

CMD ["python", "app.py"]
