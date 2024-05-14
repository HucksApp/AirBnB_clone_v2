#!/usr/bin/python3
from fabric.api import put, run, local, env
from os import path


env.hosts = ["52.3.241.47", "52.3.220.183"]


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
        return True
    except Exception as e:
        return False
