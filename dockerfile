FROM ubuntu:latest

ENV HOME /root
WORKDIR /root

COPY . .

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

EXPOSE 8099

CMD ["gunicorn", "--bind", "0.0.0.0:8099", "Server.server:app"]