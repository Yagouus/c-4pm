# Activate virtual environment
source venv/bin/activate

# Terminate all rasa and gunicorn processes running
pkill rasa
pkill gunicorn

# Launch rasa actions server
cd actions || exit
rasa run actions &
cd ..

# Deploy dash app with rasa bot
gunicorn main_server:server -b :8000 --timeout 240