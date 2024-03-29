FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./models/ ./models/

ENTRYPOINT [ "python", "./models/manage.py" ]