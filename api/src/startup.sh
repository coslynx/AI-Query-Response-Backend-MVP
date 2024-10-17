#!/bin/bash

# Set exit on error
set -e

# Load environment variables
source .env

# Create database connection
python -c "import sqlalchemy; print(sqlalchemy.create_engine('$DATABASE_URL').connect())"

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload