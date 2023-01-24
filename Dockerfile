
# syntax=docker/dockerfile:1

FROM python:3.9-buster



WORKDIR /aichallenge

COPY ./requirements.txt /aichallenge/requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get install -y openssl

RUN pip3 install -r requirements.txt

COPY . /aichallenge/

VOLUME ["/aichallenge/"]

CMD gunicorn -w 2 --threads 100 --certfile cert.pem --keyfile key.pem app:app





