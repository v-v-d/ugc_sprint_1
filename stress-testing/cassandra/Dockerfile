FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
COPY /requirements.txt ./
RUN pip3 install -r requirements.txt

ADD ./code /code

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x wait-for-it.sh

WORKDIR /code

ENV PYTHONPATH=/code

CMD ../wait-for-it.sh cassandra1:9042 -t 180 -- python main.py