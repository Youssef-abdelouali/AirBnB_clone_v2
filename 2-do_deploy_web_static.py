#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers.
"""

from datetime import datetime
from fabric.api import *
import os

# Define the hosts and user for deployment
env.hosts = ["52.91.121.146", "3.85.136.181"]
env.user = "ubuntu"


def do_pack():
    """
    Creates a .tgz archive of the web_static directory and returns its path.
    If the archive is created successfully, returns the path to the archive.
    Otherwise, returns None.
    """
    # Create the versions directory if it doesn't exist
    local("mkdir -p versions")
    
    # Generate a timestamp for the archive file name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)
    
    # Create a .tgz archive of the web_static directory
    result = local("tar -cvzf {} web_static".format(archive_path))

    # Check if the archive creation was successful
    if result.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    """
    Distributes the archive to web servers.
    If the archive exists, performs the following steps:
    1. Uploads the archive to the /tmp/ directory on the server.
    2. Creates a new directory on the server for the archive.
    3. Extracts the contents of the archive to the new directory.
    4. Deletes the temporary archive file.
    5. Moves the contents of web_static to the new directory.
    6. Removes the old web_static directory.
    7. Creates a symbolic link to the new release.
    
    Returns True if the deployment is successful, otherwise False.
    """
    if os.path.exists(archive_path):
        # Extract the file name from the archive path
        archive_file = os.path.basename(archive_path)
        release_dir = "/data/web_static/releases/{}".format(archive_file[:-4])
        temp_archive = "/tmp/{}".format(archive_file)
        
        # Upload the archive to the server
        put(archive_path, "/tmp/")
        
        # Create the release directory and extract the archive
        run("sudo mkdir -p {}".format(release_dir))
        run("sudo tar -xzf {} -C {}/".format(temp_archive, release_dir))
        
        # Remove the temporary archive and move the contents
        run("sudo rm {}".format(temp_archive))
        run("sudo mv {}/web_static/* {}".format(release_dir, release_dir))
        
        # Clean up by removing the old web_static directory and updating the symlink
        run("sudo rm -rf {}/web_static".format(release_dir))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(release_dir))
        
        print("New version deployed!")
        return True

    return False
