#!/bin/bash

# Exit immediately if any command fails
set -e  

echo "🚀 Installing dependencies..."
pip install -r requirements.txt

echo "🔄 Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
