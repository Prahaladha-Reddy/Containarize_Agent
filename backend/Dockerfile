FROM python:3.12-slim-bullseye

RUN apt-get update && apt-get install -y curl

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./src .



#RUN echo "Hello World" > index.html




CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]