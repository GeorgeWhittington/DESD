FROM python:3.11.4

WORKDIR /usr/src/smartcare_django

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install python3-pip libpango-1.0-0 libpangoft2-1.0-0 -y

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
