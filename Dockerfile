FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3.10 \
    tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    apt-get clean && rm -rf /var/lib/apt/lists/* &&\
    mkdir -p app && \
    pip3 install -U crawl4ai && \
    playwright install && \
    playwright install-deps

WORKDIR /app

COPY ./app/. .
COPY requirements.txt .

RUN pip3 install -r requirements.txt