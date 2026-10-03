FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
ENV PYTHONPATH=/app/src
CMD ["uvicorn", "pulsecast.service.api:app", "--host", "0.0.0.0", "--port", "8000"]
