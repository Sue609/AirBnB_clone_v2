#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

#Install Nginx if it not already installed
if ! command -v nginx &> /dev/null; then
	sudo apt-get update
	sudo apt-get install nginx
fi

#Create the folder /data/ if it doesn’t already exist
data_folder="/data/"

if [ ! -d "$data_folder" ]; then
	mkdir -p "$data_folder"
fi

#Create the folder /data/web_static/ if it doesn’t already exist
web_static_folder="${data_folder}/web_static"

if [ ! -d "$web_static_folder" ]; then
	mkdir -p "$web_static_folder"
fi

#Create the folder /data/web_static/releases/ if it doesn’t already exist
releases_folder="${web_static_folder}/releases"

if [ ! -d "$releases_folder" ]; then
	mkdir -p "$releases_folder"
fi

#Create the folder /data/web_static/shared/ if it doesn’t already exist
shared_folder="${web_static_folder}/shared"

if [ ! -d "$shared_folder" ]; then
	mkdir -p "$shared_folder"
fi

#Create the folder /data/web_static/releases/test/ if it doesn’t already exist
test_folder="${releases_folder}/test"

if [ ! -d "$test_folder" ]; then
	mkdir -p "$test_folder"
fi

#Create a fake HTML file /data/web_static/releases/test/index.html
index_file="${test_folder}/index.html"

if [ ! -d "$index_file" ]; then
	echo "My name is Susan" > /data/web_static/releases/test/index.html
fi

#Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder
current_link="${web_static_folder}/current"

if [ -L "$current_link" ]; then
	rm "$current_link"
fi

ln -s "$test_folder" "$current_link"

# Give ownership of the /data/ folder to the ubuntu user and group recursively

chown -R ubuntu:ubuntu "$data_folder"

#Update Nginx configuration
sed -i '/^\tserver_name/ a\\tlocation /hbnb_static \{\n\t\talias /data/web_static/current;\n\t\}\n' /etc/nginx/sites-available/default

service nginx restart
