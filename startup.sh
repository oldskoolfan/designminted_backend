#!/bin/sh

cd /var/www/dmblogapi

virtualenv dmblogapi-venv

source dmblogapi-venv/bin/activate

pip install -r requirements.txt
pip install uwsgi

uwsgi --ini /etc/uwsgi/dmblogapi.ini