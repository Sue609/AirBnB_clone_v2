#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers.
"""

from fabric.api import put,env, run, local
from os.path import exists

env.host = ['100.25.223.62', '18.204.11.178']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/private_key'


def do_deploy(archive_path):
    """
    Distribute archieve to web servers.
    """

    if not exists( archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        filename = archive_path.split("/")[-1].split(".")[0]
        release_path = "/data/web_static/releases/{}".format(filename)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{}.tgz -C {}".format(filename, release_path))

        run ("rm /tmp/{}.tgz".format(filename))

        run("mv {}/web_static/* {}".format(release_path, release_path))

        run("rm -rf {}/web_static".format(release_path))

        run("rm -rf /data/web_static/current")

        run("ln -s {} /data/web_static/current".format(release_path))

        return True
