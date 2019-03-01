#!/bin/bash

crontab ./whoismrsaemir/cronjobs
python ./whoismrsaemir/manage.py makemigrations
python ./whoismrsaemir/manage.py migrate
python ./whoismrsaemir/manage.py createsuperuser
python ./whoismrsaemir/manage.py runserver 0.0.0.0:8000
