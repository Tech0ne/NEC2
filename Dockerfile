
FROM ubuntu:22.04

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install python3 python3-pip

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "/app/main.py" ]