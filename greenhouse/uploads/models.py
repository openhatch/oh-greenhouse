from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment

class UDD(models.Model):
    connection_name='udd'
    source = models.TextField()
    version = models.TextField()
    date = models.DateTimeField(blank=True, primary_key=True)
    changed_by = models.TextField(blank=True)
    changed_by_name = models.TextField(blank=True)
    changed_by_email = models.TextField(blank=True)
    maintainer = models.TextField(blank=True)
    maintainer_name = models.TextField(blank=True)
    maintainer_email = models.TextField(blank=True)
    nmu = models.NullBooleanField(null=True, blank=True)
    signed_by = models.TextField(blank=True)
    signed_by_name = models.TextField(blank=True)
    signed_by_email = models.TextField(blank=True)
    key_id = models.TextField(blank=True)
    distribution = models.TextField(blank=True)
    file = models.TextField(blank=True)
    fingerprint = models.TextField(blank=True)

    class Meta:
        db_table = u'upload_history'
        unique_together = ('source', 'version')
        managed = False

class People(models.Model):
    connection_name='default'
    name = models.TextField(blank=True)
    email = models.EmailField(blank=True, unique=True)
    original_email = models.EmailField(null=True, default=None)
    first_upload = models.ForeignKey('Uploads', related_name='+')
    is_active = models.BooleanField(default=False)
    total_uploads = models.IntegerField(blank=True, default=0)
    last_upload = models.ForeignKey('Uploads', related_name='+')
    ubuntu_dev = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    contacts = generic.GenericRelation(Comment, object_id_field="object_pk")
    contacted = models.BooleanField(default=False)
    control_group = models.BooleanField(default=False)

    class Meta:
        db_table = u'people'

class Uploads(models.Model):
    connection_name='default'
    timestamp = models.DateTimeField(null=True, blank=True)
    release = models.TextField(blank=True)
    package = models.TextField(blank=True)
    version = models.TextField(blank=True)
    name_changer = models.TextField(blank=True)
    email_changer = models.EmailField(blank=True)
    original_email_changer = models.EmailField(null=True, default=None)
    name_sponsor = models.TextField(blank=True)
    email_sponsor = models.EmailField(blank=True)

    class Meta:
        db_table = u'uploads'
        unique_together = ('package', 'version')

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
 