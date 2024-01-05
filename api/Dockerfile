FROM python:3.10-alpine

RUN apk --no-cache add curl

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "-t", "60", "main:app"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "-t", "60", "--log-level", "debug", "main:app"]

