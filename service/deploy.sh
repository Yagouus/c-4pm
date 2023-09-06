# Activate virtual environment
source venv/bin/activate

# Terminate all rasa and gunicorn processes running
pkill rasa
pkill gunicorn

# Launch rasa actions server
cd actions || exit
rasa run actions &
cd ..

rasa run --enable-api &

# Deploy dash app with rasa bot
gunicorn wsgi:application -b :8008 --timeout 240