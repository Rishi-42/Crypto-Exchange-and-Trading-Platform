FROM python:3.8-slim-buster
ENV PYTHONUNBUFFEREED=1
WORKDIR /trading
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .