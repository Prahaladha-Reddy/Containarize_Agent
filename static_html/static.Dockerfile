FROM python:3.14.0b3-slim-bullseye

WORKDIR /app

COPY ./src .

#RUN echo "Hello World" > index.html




CMD ["python", "-m", "http.server", "8000"]