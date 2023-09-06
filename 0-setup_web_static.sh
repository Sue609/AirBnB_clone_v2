#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Update and install nginx if it's not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create necessary directories and index.html file
sudo mkdir -p /data/web_static/{releases/test,shared}

# Create a symbolic link
if [ ! -e /data/web_static/current ]; then
    sudo ln -s /data/web_static/releases/test /data/web_static/current
fi

# Set ownership
sudo chown -R ubuntu:ubuntu /data/

config_file="/etc/nginx/sites-available/default"
if ! grep -q 'location /hbnb_static/' "$config_file"; then
    sudo sed -i '/server_name _;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' "$config_file"
fi

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By \"$HOSTNAME\";
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
	alias /data/web_static/current;
	index index.html index.htm;
    }

    location /redirect_me {
	return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

sudo service nginx restart

exit 0
