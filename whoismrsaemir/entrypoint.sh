#!/bin/bash

crontab ./whoismrsaemir/cronjobs
service cron start
mkdir -p ./whoismrsaemir/database
#python3 ./whoismrsaemir/manage.py makemigrations
python3 ./whoismrsaemir/manage.py migrate
#python3 ./whoismrsaemir/manage.py runserver 0.0.0.0:8000
