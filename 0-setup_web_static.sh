#!/usr/bin/ env bash
#  Bash script that sets up your web servers for the deployment of web_static

if ! dpkg | grep -q nginx; then
	sudo apt-get update
	sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/{releases/test,shared}
sudo touch /mkdir/web_static/releases/test/index.html

echo "My name is Susan!" > | sudo tee /data/web_static/releases/test/index.html

sudo rm -f /data/web_static_current
sudo ln -s /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config_file="/etc/nginx/sites-available/default"

if ! grep -q 'location /hbnb_static/' "$config_file"; then
	sudo sed -i '/server_name _;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' "$config_file"
fi

sudo service nginx restart

exit 0
