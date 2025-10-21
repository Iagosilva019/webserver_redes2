FROM ubuntu:24.04

RUN apt update && apt install -y python3 python3-pip iputils-ping net-tools

WORKDIR /app

COPY . .

CMD ["python3", "--version"]
