#!/usr/bin/env bash
# Script to set up web servers for deploying web_static

# Update and install Nginx
sudo apt-get update
sudo apt-get install -y nginx

# Allow HTTP traffic through the firewall
sudo ufw allow 'Nginx HTTP'

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a sample HTML file in the test directory
echo "<html>
  <head></head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link to the current release
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of the /data/ directory to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve content from the /hbnb_static/ alias
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/; }' /etc/nginx/sites-enabled/default

# Restart Nginx to apply the changes
sudo service nginx restart
