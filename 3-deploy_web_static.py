#!/usr/bin/python3
"""
script that creates and distributes an archive to your webservers.
"""

from fabric.api import env, run, local, put
from os.path import exists
from datetime import datetime


env.hosts = ['100.25.223.62', '18.204.11.178']
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

    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')
        filename = archive_path.split("/")[-1].split(".")[0]
        release_path = "/data/web_static/releases/{}".format(filename)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{}.tgz -C {}".format(filename, release_path))
        run("rm /tmp/{}.tgz".format(filename))
        run("mv {}/web_static/* {}".format(release_path, release_path))
        run("rm -rf {}/web_static".format(release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_path))
        return True
    except Exception as e:
        return False


def deploy():
    """
    Deploy the web_static archive to web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
