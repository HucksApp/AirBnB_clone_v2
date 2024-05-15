#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
from fabric.api import env, local, run
import os

env.hosts = ["52.3.241.47", "52.3.220.183"]
env.user = 'ubuntu'


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = int(number)
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    local("cd versions && ls -t | tail -n +{} | xargs rm -f".format(number))

    run("cd /data/web_static/releases && ls -t | tail -n +{} | xargs rm -rf"
        .format(number))
