FROM python:3.7-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /hotels
COPY requirements.txt .
RUN set -ex\
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
ADD . .