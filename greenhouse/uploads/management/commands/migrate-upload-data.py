from django.core.management.base import NoArgsCommand
from django.core.exceptions import ObjectDoesNotExist
from uploads.common.launchpad import lp_login as lp
from django.db import connections
from uploads.models import Uploads


class Command(NoArgsCommand):
    help = "Migrate upload data from UDD to django managed database."

    def import_uploads(self):
        cursor = connections['udd'].cursor()
        sql = """SELECT date, distribution, source, version, changed_by_name,
                 changed_by_email, signed_by_name, signed_by_email
                 FROM upload_history ORDER BY date"""
        cursor.execute(sql)
        try:
            t = 'timestamp'
            latest_entry = Uploads.objects.values(t).latest(t)[t]
        except ObjectDoesNotExist:
            latest_entry = None
        for row in self.row_iter(cursor):
            if latest_entry is None or row[0] > latest_entry:
                if row[4] == row[6] or row[5] == row[7]:
                    spon_email = ''
                    spon_name = ''
                else:
                    spon_name = row[6]
                    spon_email = row[7]
                uploads = Uploads(timestamp=row[0], release=row[1],
                                  package=row[2], version=row[3],
                                  name_changer=row[4], email_changer=row[5],
                                  original_email_changer=row[5],
                                  name_sponsor=spon_name,
                                  email_sponsor=spon_email,)
                uploads.save()
        cursor.close()

        # Change the email for all new uploads
        # of people who are not authoritative
        for p in People.objects.filter(authoritative=False):
            for u in Uploads.objects.filter(
                    timestamp__gte=latest_entry).filter(
                    email_changer=p.original_email):
                u.email_changer = p.email
                u.save()

    def row_iter(self, cursor, size=1000):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def handle_noargs(self, **options):
        self.import_uploads()
