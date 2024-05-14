#!/usr/bin/python3
"""
Distributes an archive to my web servers,
using the function deploy
"""

from fabric.api import put, run, local, env
from time import strftime
from datetime import date
from os import path

env.hosts = ["52.3.241.47", "52.3.220.183"]
env.user = 'ubuntu'


def do_pack():
    """ A script that generates archive the contents of web_static folder"""

    filename = strftime("%Y%m%d%H%M%S")
    try:
        local("sudo mkdir -p versions")
        local("sudo tar -czvf versions/web_static_{}.tgz web_static/"
              .format(filename))
        archive_path = "versions/web_static_{}.tgz".format(filename)
        print('web_static packed: {} -> {}'.format(archive_path,
              path.getsize(archive_path)))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Fabric script that distributes
    an archive to your web server"""

    if not path.exists(archive_path):
        return False
    try:
        tgzfile = archive_path.split("/")[-1]
        print(tgzfile)
        filename = tgzfile.split(".")[0]
        print(filename)
        pathname = "/data/web_static/releases/" + filename
        put(archive_path, '/tmp/')
        run("sudo mkdir -p /data/web_static/releases/{}/".format(filename))
        run("sudo tar -zxvf /tmp/{} -C /data/web_static/releases/{}/"
            .format(tgzfile, filename))
        run("sudo rm /tmp/{}".format(tgzfile))
        run("sudo mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(filename, filename))
        run("sudo rm -rf /data/web_static/releases/{}/web_static"
            .format(filename))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))
        print('New version deployed!')
        return True
    except Exception as e:
        return False


def deploy():
    """run the 2 functions"""

    path = do_pack()
    if not path:
        return False

    return do_deploy(path)
