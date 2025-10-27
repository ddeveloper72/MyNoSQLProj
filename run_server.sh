#!/bin/bash
# Activate virtual environment and run Django server

echo "Activating virtual environment..."
source .venv/Scripts/activate

echo "Virtual environment activated. Python path:"
which python

echo "Installing/checking dependencies..."
pip install django pymongo python-dotenv mongoengine

echo "Starting Django development server..."
python manage.py runserver