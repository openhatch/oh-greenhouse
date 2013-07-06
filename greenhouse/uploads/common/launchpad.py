from django.conf import settings
from launchpadlib.launchpad import Launchpad
import sys

def lp_login(consumer, anonymous=True, lp_service='production'):
    cachedir = settings.CACHE_PATH
    try:
        if anonymous:
            launchpad = Launchpad.login_anonymously(consumer, lp_service, cachedir)
        else:
            launchpad = Launchpad.login_with(consumer, lp_service, cachedir)
    except:
        launchpad = None
        print sys.stderr, "No Launchpad connection."
    return launchpad
