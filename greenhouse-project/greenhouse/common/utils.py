import datetime
import errno
import fcntl
import os

from django.core import management
from django.conf import settings


def lock_path(path):
    f = open(path, "wb")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return f
    except IOError, e:
        if e.errno in (errno.EACCES, errno.EAGAIN):
            return None
        raise


def update_stamp(stamp_file):
    open(stamp_file, "a").close()
    os.utime(stamp_file, None)


def run_cmd(cmd, interval):
    stamp_dir = settings.TEMP_PATH
    if not os.path.exists(stamp_dir):
        os.makedirs(stamp_dir)
    stamp_file = os.path.join(stamp_dir, "%s.stamp" % cmd)
    lock_file = os.path.join(stamp_dir, "%s.lock" % cmd)
    if not os.path.exists(stamp_file) or datetime.datetime.utcfromtimestamp(
       os.path.getmtime(stamp_file)) + interval < datetime.datetime.now():
        f = lock_path(lock_file)
        if f:
            management.call_command(cmd)
            update_stamp(stamp_file)
