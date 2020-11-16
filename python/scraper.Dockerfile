FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && mkdir -p /data/scraped/

COPY ./scraper/ .

COPY ./models/ ./

ENTRYPOINT [ "python", "./main.py" ]