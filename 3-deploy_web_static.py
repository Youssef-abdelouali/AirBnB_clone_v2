#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.

import os
from datetime import datetime
from fabric.api import env, local, put, run

# Define the hosts for deployment
env.hosts = ["52.91.121.146", "3.85.136.181"]

def do_pack():
    """Create a tar.gz archive of the web_static directory."""
    dt = datetime.utcnow()
    archive_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )
    
    # Create the versions directory if it doesn't exist
    if not os.path.isdir("versions"):
        if local("mkdir -p versions", capture=True).failed:
            return None
    
    # Create the archive
    if local("tar -cvzf {} web_static".format(archive_name), capture=True).failed:
        return None
    
    return archive_name

def do_deploy(archive_path):
    """Distribute an archive to the web servers.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        bool: True if the deployment succeeded, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False
    
    # Extract the file name and name without extension
    file_name = os.path.basename(archive_path)
    name = file_name.split(".")[0]
    
    # Upload the archive to the server
    if put(archive_path, "/tmp/{}".format(file_name)).failed:
        return False
    
    # Create the release directory and extract the archive
    release_dir = "/data/web_static/releases/{}".format(name)
    if run("rm -rf {}".format(release_dir)).failed:
        return False
    if run("mkdir -p {}".format(release_dir)).failed:
        return False
    if run("tar -xzf /tmp/{} -C {}".format(file_name, release_dir)).failed:
        return False
    
    # Clean up temporary files and update symlink
    if run("rm /tmp/{}".format(file_name)).failed:
        return False
    if run("mv {}/web_static/* {}".format(release_dir, release_dir)).failed:
        return False
    if run("rm -rf {}/web_static".format(release_dir)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s {} /data/web_static/current".format(release_dir)).failed:
        return False
    
    return True

def deploy():
    """Create and distribute an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
