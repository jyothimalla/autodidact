#!/bin/bash

# ⚙️ Build Angular frontend
echo "📦 Building Angular app..."
ng build --configuration production

# 📤 Copy to VPS
echo "🚀 Uploading build to VPS..."
scp -r dist/autodidact-frontend/browser/* ubuntu@51.38.234.237:/tmp/latest-frontend/

# 🖥️ SSH into VPS and deploy to NGINX
echo "🛠️ Updating NGINX on VPS..."
ssh ubuntu@51.38.234.237 << 'ENDSSH'
  sudo rm -rf /var/www/html/*
  sudo cp -r /tmp/latest-frontend/* /var/www/html/
  sudo systemctl restart nginx
  echo "✅ Deployment complete!"
ENDSSH
