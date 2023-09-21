#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import local, run, cd, env
from datetime import datetime
import os


env.hosts = ['100.25.223.62', '18.204.11.178']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/private_key'


def do_clean(number=0):
    """
    Delete out-of-date archives.
    """
    try:
        number = int(number)
        if number < 0:
            number = 0

        local_archives = sorted(os.listdir('versions'))
        if number == 0 or number == 1:
            to_delete = local_archives[:-1]
        else:
            to_delete = local_archives[:-number]

        for archive in to_delete:
            local('rm -f versions/{}'.format(archive))

        with cd('/data/web_static/releases'):
            remote_archives = run('ls -1').split('\n')

        if number == 0 or number == 1:
            to_delete = remote_archives[:-1]
        else:
            to_delete = remote_archives[:-number]

        for archive in to_delete:
            run('rm -f /data/web_static/releases/{}'.format(archive))
    except ValueError:
        pass
