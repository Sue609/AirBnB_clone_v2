#!/usr/bin/python3
"""
This module introduces a fabric script.
"""

from datetime import datetime
import os
from fabric.api import local


def do_pack():
    """
    Fabric script that generates a .tgz archive from the contents
    of the web_static folder
    of your AirBnB Clone repo, using the function do_pack.
    """
    if not os.path.exists("versions"):
        local("mkdir versions")

    date = datetime.now()
    name_of_archive = "versions/web_static_{}.tgz".format(
            date.strftime("%Y%m%d%H%M%S")
    )

    command = "tar -cvzf {} {}".format(name_of_archive, "web_static")

    output = local(command)

    if not output.failed:
        return name_of_archive
