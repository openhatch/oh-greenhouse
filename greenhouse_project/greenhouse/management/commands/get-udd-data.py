import subprocess
import sys
import os
import urllib

from django.core.management.base import NoArgsCommand
from django.conf import settings
import psycopg2 as db

URL = "http://alioth.debian.org/~asb/udd/ubuntu_upload_history.sql"
LOCAL_FILE = os.path.join(settings.TEMP_PATH, "udd.sql")
UPDATED_FILE = os.path.join(settings.TEMP_PATH, "new-udd.sql")


class Command(NoArgsCommand):
    help = "Update uploads data from UDD."

    def get_new_udd_data(self):
        try:
            sock = urllib.urlopen(URL)
            urllib.urlretrieve(URL, UPDATED_FILE)
            if os.path.exists(LOCAL_FILE):
                os.remove(LOCAL_FILE)
            os.rename(UPDATED_FILE, LOCAL_FILE)
        except:
            return None
        sock.close()
        return LOCAL_FILE

    def handle_noargs(self, **options):
        #new_script = self.get_new_udd_data()
        new_script = LOCAL_FILE
        if not new_script:
            sys.exit(1)
        dbinfo = settings.DATABASES['udd']
        conn = db.connect(host=dbinfo['HOST'], dbname='postgres',
                          user=dbinfo['USER'], password=dbinfo['PASSWORD'],
                          port=dbinfo['PORT'] or 5432)
        cursor = conn.cursor()
        conn.set_isolation_level(0)
        cursor.execute("DROP DATABASE IF EXISTS " + dbinfo['NAME'])
        cursor.execute("CREATE DATABASE " + dbinfo['NAME'] +
                       " WITH TEMPLATE=template0 ENCODING 'SQL_ASCII'")
        conn.commit()
        cursor.close()
        conn.close()

        conn = db.connect(host=dbinfo['HOST'], dbname=dbinfo['NAME'],
                          user=dbinfo['USER'], password=dbinfo['PASSWORD'],
                          port=dbinfo['PORT'] or 5432)
        cursor = conn.cursor()
        cursor.execute("CREATE EXTENSION IF NOT EXISTS debversion")
        conn.commit()
        cursor.close()
        conn.close()

        psql_env = os.environ.copy()
        psql_env['PGPASSWORD'] = dbinfo['PASSWORD']
        psql_cmd = ['psql',
                    '-U', dbinfo['USER'],
                    '-d', dbinfo['NAME'],
                    '-f', new_script]
        subprocess.call(psql_cmd, env=psql_env)
