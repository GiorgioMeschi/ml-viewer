# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY . /app

# ensure credentials.yaml is mounted at runtime; default path inside container
ENV CREDENTIALS_PATH=/app/credentials.yaml

# expose streamlit default port
EXPOSE 8501

# run streamlit (use your main entry file; you wrote HOME.py)
ENTRYPOINT  ["streamlit", "run", "HOME.py", "--server.port=8501", "--server.address=0.0.0.0"]
