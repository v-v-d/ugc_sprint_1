#!/bin/sh

# wait for Kafka to start, then run the server
chmod +x ../wait-for-it.sh
exec ../wait-for-it.sh broker:9092 -t 60 -- python manage.py runserver