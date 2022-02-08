FROM python:3.9-slim AS base
ENV PYTHONUNBUFFERED 1
COPY requirements/*.txt ./
RUN pip3 install -r stress-testing.txt

