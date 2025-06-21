FROM python:3.14.0b3-slim-bullseye

CMD ["python", "-m", "http.server", "8000"]