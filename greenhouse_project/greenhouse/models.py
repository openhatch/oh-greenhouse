from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment


class UDD(models.Model):
    connection_name = 'udd'
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
    connection_name = 'default'
    name = models.TextField(blank=True)
    email = models.EmailField(db_index=True)
    original_email = models.EmailField(unique=True)
    first_upload = models.ForeignKey('Uploads', related_name='+')
    total_uploads = models.IntegerField(blank=True, default=0)
    last_upload = models.ForeignKey('Uploads', related_name='+')
    ubuntu_dev = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    contacts = generic.GenericRelation(Comment, object_id_field="object_pk")
    contacted = models.BooleanField(default=False)
    control_group = models.BooleanField(default=False)
    authoritative = models.BooleanField(default=True)

    def merge(self, other):
        self.email = other.email
        self.authoritative = False

        if self.first_upload.timestamp < other.first_upload.timestamp:
            other.first_upload = self.first_upload
        other.total_uploads += self.total_uploads
        if self.last_upload.timestamp > other.last_upload.timestamp:
            other.last_upload = self.last_upload
        if self.ubuntu_dev:
            other.ubuntu_dev = True
        if self.notes:
            other.notes = ''.join(["\nnotes from merged identity with email ",
                                   self.original_email, "\n", self.notes])
        for contact in self.contacts.all():
            other.contacts.add(contact)

        self.save()
        other.save()

        for upload in Uploads.objects.filter(email_changer=self.email):
            upload.email_changer = other.email
            upload.save()

class Uploads(models.Model):
    connection_name = 'default'
    timestamp = models.DateTimeField(null=True, blank=True)
    release = models.TextField(blank=True)
    package = models.TextField(blank=True)
    version = models.TextField(blank=True)
    name_changer = models.TextField(blank=True)
    email_changer = models.EmailField(db_index=True, blank=True)
    original_email_changer = models.EmailField(blank=True)
    name_sponsor = models.TextField(blank=True)
    email_sponsor = models.EmailField(blank=True)

    class Meta:
        unique_together = ('package', 'version')


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
