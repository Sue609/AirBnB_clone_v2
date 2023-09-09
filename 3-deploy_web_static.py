#!/usr/bin/python3
"""
script that creates and distributes an archive to your webservers.
"""

from fabric.api import env, run, local, put
from os.path import exists
from datetime import datetime
import os.path


env.hosts = ['52.204.104.109', '34.234.204.154']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/private_key'


def do_pack():
    """
    Creates a compressed archive of the web_static folder.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    local("mkdir -p versions")
    result = local("tar -cvzf {} web_static".format(archive_name))

    if result.succeeded:
        return archive_name
    else:
        return None


def do_deploy(archive_path):
    """
    Distribute archive to web servers.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """
    Deploy the web_static archive to web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
