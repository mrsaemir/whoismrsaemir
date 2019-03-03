#!/bin/bash

crontab ./whoismrsaemir/cronjobs
python3 ./whoismrsaemir/manage.py makemigrations
python3 ./whoismrsaemir/manage.py migrate
python3 ./whoismrsaemir/manage.py createsuperuser
python3 ./whoismrsaemir/manage.py runserver 0.0.0.0:8000
