#!/bin/bash
set -e  # Exit immediately on error

echo "🚀 Deployment started ..."

# Navigate to project directory
cd ~/COCOMATIK/BackEnd || { echo "❌ Failed to navigate to BackEnd directory"; exit 1; }

# Pull latest changes
echo "📦 Pulling latest changes..."
git pull origin master
echo "✅ New changes copied to server!"

# Check if virtual environment exists, if not create it
if [ ! -d "zenv" ]; then
    echo "🛠️ Virtual environment 'zenv' not found, creating one..."
    python3 -m venv zenv
    echo "✅ Virtual environment 'zenv' created!"
fi

# Activate Virtual Environment
echo "🐍 Activating Virtual Environment..."
source zenv/bin/activate
echo "✅ Virtual env 'zenv' Activated!"

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Clearing Cache
echo "🗑️ Clearing Cache..."
find . -name "*.pyc" -delete
python manage.py clear_cache || echo "⚠️ No clear_cache command found, skipping."

# Install Dependencies
echo "📦 Installing Dependencies..."
pip install -r requirements.txt --no-input

# Collect Static Files
echo "🎨 Collecting Static Files..."
python manage.py collectstatic --noinput

# Run Migrations
echo "🔄 Running Database Migration..."
python manage.py migrate

# Deactivate Virtual Environment
deactivate
echo "✅ Virtual env 'zenv' Deactivated!"

# Restart Gunicorn
echo "🔄 Reloading Gunicorn..."
pkill -HUP -f "gunicorn" || echo "⚠️ Gunicorn process not found, starting a new one..."
echo "✅ Deployment Finished!"
