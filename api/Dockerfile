FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libc-dev libpq-dev

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3000

EXPOSE 3000

CMD ["flask", "run"]