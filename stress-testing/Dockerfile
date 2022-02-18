FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
COPY /stress-testing/requirements.txt ./
RUN pip3 install -r requirements.txt

ADD ./stress-testing /code

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x wait-for-it.sh

WORKDIR /code

ENV PYTHONPATH=/code

CMD ../wait-for-it.sh clickhouse-node1:8123 -t 60 -- python main.py