from django.core.management.base import NoArgsCommand
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.utils import timezone

import os
import gc
import re
import random

from greenhouse.models import UDD, Person, Activity


class Command(NoArgsCommand):
    help = "Migrate upload data from UDD to django managed database."
    
    def get_debian_emails(self):
        exclude_file = os.path.join(settings.PROJECT_PATH, 'debian-emails')
        with open(exclude_file) as f:
            return set(email.strip() for email in f)


    def import_person(self):
        bulk_insert_person = []
        exclude_emails = self.get_debian_emails()
        person_set = set(Person.objects.values_list('email', flat=True))
        for u in UDD.objects.values_list('changed_by_name', 'changed_by_email').distinct():
            email = u.changed_by_email
            if email not in person_set:
                control_group = True if random.randint(1,10) > 8 else False
                exclude = True if (email in exclude_emails or 
                               re.search(r"@debian\.org", email)) else False
                person = Person(email=email,
                                name=u.changed_by_name,
                                control_group=control_group,
                                exclude=exclude,
                                authoritative_person=None
                                )
                bulk_insert_person.append(person)
        Person.objects.bulk_create(bulk_insert_person)


    def import_uploads(self):
        CHUNK_SIZE = 5000
        person_table = {person.email: person for person in Person.objects.all()}
        try:
            now = UDD.objects.filter(date__lt=timezone.now()).latest('date').date
            current = Activity.objects.latest('time').time
        except ObjectDoesNotExist:
            current = UDD.objects.order_by('date')[0].date
      
        while current < now:
            bulk_insert_activity = []
            for u in UDD.objects.filter(date__gt=current).filter(date__lte=now
                                        ).order_by('date')[:CHUNK_SIZE]:    
                email = u.changed_by_email
                person = person_table[email]
                activity = Activity(time=u.date,
                                    person=person,
                                    original_person=person,
                                    type="upload_package",
                                    subproject=u.source + " " + u.version,
                                    )
                bulk_insert_activity.append(activity)                         
            Activity.objects.bulk_create(bulk_insert_activity)
            current = u.date        
            gc.collect()

        # Change the person for uploads of people who are not authoritative
        for p in Person.objects.filter(authoritative_person__isnull=False):
            Activity.objects.filter(person=p.original_person).update(person=p.person)

    def handle_noargs(self, **options):
        self.import_person()
        self.import_uploads()
