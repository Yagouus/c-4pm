#!/bin/bash

# Activate virtual environment
cd /home/citius/c-4pm || exit
source venv/bin/activate

# Terminate all rasa and gunicorn processes running
pkill rasa
pkill gunicorn

# Launch rasa actions server
cd actions || exit
rasa run actions &

# Launch rasa server
cd ..
rasa run --enable-api &

# Deploy dash app with rasa bot
gunicorn wsgi:application -b :8000 --timeout 240