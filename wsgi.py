import os
import sys
import django.core.handlers.wsgi
project_path = os.path.join(os.path.dirname(__file__), 'greenhouse')
sys.path.insert(0, os.path.abspath(project_path))
os.environ['DJANGO_SETTINGS_MODULE'] = 'greenhouse.settings'
application = django.core.handlers.wsgi.WSGIHandler()
