from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import Group
from django.conf import settings


class Command(NoArgsCommand):
    help = "Set up initial Djano User Groups that match LP teams."

    def handle_noargs(self, **options):
        for team in settings.ALLOWED_LAUNCHPAD_TEAMS:
            group, created = Group.objects.get_or_create(name=team)
