#!/usr/bin/python3
"""
Distributes an archive to my web servers,
using the function deploy
"""

from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ["52.3.241.47", "52.3.220.183"]
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    try:
        local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(
            datetime.now().strftime("%Y%m%d%H%M%S"))
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        file_name = archive_path.split("/")[-1].split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(file_name))
        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(file_name, file_name))
        run("rm /tmp/{}.tgz".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(file_name, file_name))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(file_name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(file_name))
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """Creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
