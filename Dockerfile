FROM python:3.10-slim

WORKDIR /code
RUN apt-get update -y  \
    && apt-get autoclean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
COPY . .
EXPOSE 7000

CMD gunicorn --config gunicorn.conf.py wsgi:app