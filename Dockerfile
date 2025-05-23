FROM public.ecr.aws/docker/library/python:3.11-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV PYTHONPATH=/app
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

CMD ["sh", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:5000 wsgi:app"]