FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./computer/ .

COPY ./models/ ./

ENTRYPOINT [ "python", "./main.py" ]