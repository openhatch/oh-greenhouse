from uploads.models import Uploads, People
from django.core.management.base import NoArgsCommand
from datetime import timedelta
from django.utils import timezone
from uploads.common.launchpad import lp_login as lp
from django.conf import settings
import os, re, random

class Command(NoArgsCommand):
    help = "Create entry in people table if new LP id is found in uploads table."

    def import_people(self):
        blacklist = ['katie', 'ps-jenkins', 'ubuntu-langpack',
                     'kubuntu-members', '']

        debian_devs_email_file = os.path.join(settings.PROJECT_PATH, 'debian-emails')
        debian_devs_email_set = set()
        with open(debian_devs_email_file) as f:
            for email in f:
                debian_devs_email_set.add(email.strip())
                                
        emails = Uploads.objects.values_list('email_changer', flat=True).distinct()
        for email in emails.exclude(email_changer__in=blacklist):
            first_ul = Uploads.objects.filter(email_changer=email).earliest('timestamp')
            last_ul = Uploads.objects.filter(email_changer=email).latest('timestamp')

            if email in debian_devs_email_set or re.search(r"@debian\.org", email):
                debian_dev = True
            else:
                debian_dev = False
                
            if random.randint(1,10) > 8:
                control_group = True
            else:
                control_group = False
                
            person, created = People.objects.get_or_create(original_email=email,
                                                        defaults={
                                                        'name':last_ul.name_changer,
                                                        'email':last_ul.email_changer,
                                                        'first_upload':first_ul,
                                                        'last_upload':last_ul, 
                                                        'ubuntu_dev': debian_dev, 
                                                        'control_group': control_group
                                                        })

            if not created:
                person.first_upload = first_ul
                person.last_upload = last_ul
                person.ubuntu_dev = person.ubuntu_dev or debian_dev
                person.save()
            
    def total_uploads(self):
        for p in People.objects.all():
            all_uploads = Uploads.objects.filter(email_changer=p.email)
            total_uploads = len(all_uploads)
            if p.total_uploads != total_uploads:
                p.total_uploads = total_uploads
                p.save()

    def last_seen(self):
        for p in People.objects.all():
            last_ul = Uploads.objects.filter(email_changer=p.email).order_by('timestamp').reverse()[0]
            if p.last_upload != last_ul:
                p.last_upload = last_ul
                p.save()

    def is_ubuntu_dev(self):
        launchpad = lp('d-a-t', anonymous=True, lp_service='production')
        ubuntu_devs = [a.name for a in launchpad.people['ubuntu-dev'].participants] #alternative?
        #separate management command to see if debian 
        for p in People.objects.all():
            if p.email in ubuntu_devs and p.ubuntu_dev is not True:
                p.ubuntu_dev = True
                p.save()
            elif p.email not in ubuntu_devs and p.ubuntu_dev is not False:
                p.ubuntu_dev = False
                p.save()

    def handle_noargs(self, **options):
        self.import_people()
        #self.check_is_active()
        self.total_uploads()
        self.last_seen()
        #self.is_ubuntu_dev()
