from django.core.management.base import NoArgsCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections
from django.utils import timezone
import gc
from greenhouse.models import UDD, People, Uploads


class Command(NoArgsCommand):
    help = "Migrate upload data from UDD to django managed database."

    def import_uploads(self):
        CHUNK_SIZE = 5000
        try:
            now = UDD.objects.order_by('date').filter(
                date__lte=timezone.now()).reverse()[0].date
            current = latest = Uploads.objects.latest('timestamp').timestamp
        except ObjectDoesNotExist:
            current = latest = UDD.objects.order_by('date')[0].date
        while current < now:
            for u in UDD.objects.order_by(
                    'date').filter(date__gt=current)[:CHUNK_SIZE]:
                if u.date < now:
                    uploads = Uploads(timestamp=u.date,
                                      release=u.distribution,
                                      package=u.source, version=u.version,
                                      name_changer=u.changed_by_name,
                                      email_changer=u.changed_by_email,
                                      original_email_changer=
                                      u.changed_by_email,
                                      name_sponsor=u.signed_by_name,
                                      email_sponsor=u.signed_by_email)
                    uploads.save()
                    current = u.date
            gc.collect()

        # Change the email for all new uploads
        # of people who are not authoritative
        for p in People.objects.filter(authoritative=False):
            for u in Uploads.objects.filter(
                    timestamp__gte=latest).filter(
                    email_changer=p.original_email):
                u.email_changer = p.email
                u.save()

    def handle_noargs(self, **options):
        self.import_uploads()
