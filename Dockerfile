FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask prometheus_client
CMD ["python", "main.py"]
