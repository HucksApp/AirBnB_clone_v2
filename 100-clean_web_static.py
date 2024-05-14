#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

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
    if number in [0, 1]:
        number = 1

    archives = sorted(os.listdir("versions"))
    if len(archives) > number:
        [archives.pop() for i in range(number)]
        with lcd("versions"):
            [local("sudo rm ./{}".format(a)) for a in archives]

        with cd("/data/web_static/releases"):
            archives = run("sudo ls -tr").split()
            archives = [a for a in archives if "web_static_" in a]
            [archives.pop() for i in range(number)]
            [run("sudo rm -rf ./{}".format(a)) for a in archives]
