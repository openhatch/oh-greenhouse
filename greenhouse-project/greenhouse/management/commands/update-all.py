#!/usr/bin/python

import datetime
from greenhouse.common.utils import run_cmd
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = "Update all."

    def handle_noargs(self, **options):
        run_cmd("get-udd-data", datetime.timedelta(days=1))
        run_cmd("migrate-upload-data", datetime.timedelta(days=1))
        run_cmd("build_people_db", datetime.timedelta(days=1))
