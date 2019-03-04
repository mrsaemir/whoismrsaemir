#!/bin/bash

crontab ./whoismrsaemir/cronjobs
service cron start
python3 ./whoismrsaemir/manage.py makemigrations
python3 ./whoismrsaemir/manage.py migrate
python3 ./whoismrsaemir/manage.py createsuperuser
python3 ./whoismrsaemir/manage.py runserver 0.0.0.0:8000
