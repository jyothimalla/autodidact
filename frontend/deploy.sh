#!/bin/bash
echo "Building Angular project..."
ng build --configuration production

echo "Uploading build to VPS..."
scp -r ./dist/autodidact-frontend/browser/* ubuntu@51.38.234.237:/var/www/html/

echo "Restarting Nginx..."
ssh ubuntu@51.38.234.237 "sudo systemctl restart nginx"

echo "✅ Deployment complete. Check https://autodidact.uk"
