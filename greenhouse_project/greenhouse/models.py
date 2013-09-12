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


class Person(models.Model):
    connection_name = 'default'
    name = models.TextField(blank=True)
    email = models.EmailField(db_index=True)
    exclude = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    contacts = generic.GenericRelation(Comment, object_id_field="object_pk")
    control_group = models.BooleanField(default=False)
    authoritative_person = models.ForeignKey('self', null=True, default=None)

    def merge(self, other):
        self.authoritative_person = other

        if self.exclude:
            other.exclude = True
        if self.notes:
            other.notes = ''.join(["\nnotes from merged identity with email ",
                                   self.email, "\n", self.notes])
        for contact in self.contacts.all():
            other.contacts.add(contact)

        self.save()
        other.save()

        for upload in Activity.objects.filter(person=self):
            upload.person = other
            upload.save()


class Activity(models.Model):
    connection_name = 'default'
    type = models.CharField(max_length=128)
    subproject = models.CharField(max_length=128)
    time = models.DateTimeField(null=True, blank=True)
    
    package = models.TextField(blank=True)
    version = models.TextField(blank=True)

    original_person = models.ForeignKey('Person', related_name='+', null=True)
    person = models.ForeignKey('Person', related_name='activities', null=True)

    class Meta:
        unique_together = ('package', 'version')


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
