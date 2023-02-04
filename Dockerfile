# syntax=docker/dockerfile:1

FROM tensorflow/tensorflow:latest-gpu

WORKDIR /aichallenge

COPY ./requirements.txt /aichallenge/requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get install -y openssl

RUN pip3 install -r requirements.txt

COPY . /aichallenge/

VOLUME ["/aichallenge/"]

CMD python3 app.py

