#!/bin/bash
set -e  # Exit immediately on error

echo "🚀 Deployment started ..."

# Navigate to project directory
cd ~/COCOMATIK/BackEnd || { echo "❌ Failed to navigate to BackEnd directory"; exit 1; }

# Safe Git Pull
echo "📦 Pulling latest changes..."
git reset --hard HEAD
git pull origin master --rebase
echo "✅ New changes copied to server!"

# Ensure Virtual Environment Exists
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
python manage.py migrate --noinput

# Deactivate Virtual Environment
deactivate
echo "✅ Virtual env 'zenv' Deactivated!"

# Reload Gunicorn & Nginx for Zero Downtime
echo "🔄 Reloading Services..."
sudo systemctl reload nginx
sudo systemctl reload engine.cocomatik.com.gunicorn.service
sudo systemctl reload admin.cocomatik.com.gunicorn.service
echo "✅ Deployment Finished!"