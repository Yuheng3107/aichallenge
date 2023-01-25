
# syntax=docker/dockerfile:1

FROM python:3.9-buster



WORKDIR /aichallenge

COPY ./requirements.txt /aichallenge/requirements.txt

RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN apt-get install -y openssl

RUN pip3 install -r requirements.txt
RUN pip3 install tensorflow-cpu

COPY . /aichallenge/

VOLUME ["/aichallenge/"]

CMD python3 app.py

# docker run -v /Users/yuheng3107/Desktop/aichallenge:/aichallenge/ -p 5000:5000 yuheng3107/aichallenge python3 app.py
# This command works for some reason

