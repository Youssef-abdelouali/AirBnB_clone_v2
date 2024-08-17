#!/usr/bin/python3
"""A Fabric script module that creates a .tgz archive of static files."""
import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """Creates an archive from the contents of the web_static folder."""
    if not os.path.exists("versions"):
        os.makedirs("versions")
    
    current_time = datetime.now()
    archive_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        current_time.year,
        current_time.month,
        current_time.day,
        current_time.hour,
        current_time.minute,
        current_time.second
    )

    try:
        print("Packing web_static to {}".format(archive_name))
        local("tar -cvzf {} web_static".format(archive_name))
        archive_size = os.path.getsize(archive_name)
        print("web_static packed: {} -> {} Bytes".format(archive_name, archive_size))
    except Exception:
        archive_name = None
    
    return archive_name
