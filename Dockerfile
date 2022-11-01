# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 5000

ENV key=dev



# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements

WORKDIR /app
COPY . /app

COPY requirements.txt ./app
RUN  python -m pip install -r requirements.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
  RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
  USER appuser

# # During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
 CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]


