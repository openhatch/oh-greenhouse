# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Uploads', fields ['package', 'version']
        db.delete_unique(u'greenhouse_uploads', ['package', 'version'])

        # Deleting model 'Uploads'
        db.delete_table(u'greenhouse_uploads')

        # Deleting model 'People'
        db.delete_table(u'greenhouse_people')

        # Adding model 'Activity'
        db.create_table(u'greenhouse_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('subproject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('package', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('version', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('original_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['greenhouse.Person'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['greenhouse.Person'])),
        ))
        db.send_create_signal(u'greenhouse', ['Activity'])

        # Adding unique constraint on 'Activity', fields ['package', 'version']
        db.create_unique(u'greenhouse_activity', ['package', 'version'])

        # Adding model 'Person'
        db.create_table(u'greenhouse_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            ('exclude', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('control_group', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('authoritative_person', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['greenhouse.Person'], null=True)),
        ))
        db.send_create_signal(u'greenhouse', ['Person'])


    def backwards(self, orm):
        # Removing unique constraint on 'Activity', fields ['package', 'version']
        db.delete_unique(u'greenhouse_activity', ['package', 'version'])

        # Adding model 'Uploads'
        db.create_table(u'greenhouse_uploads', (
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['greenhouse.People'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('package', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('original_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', null=True, to=orm['greenhouse.People'])),
            ('subproject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'greenhouse', ['Uploads'])

        # Adding unique constraint on 'Uploads', fields ['package', 'version']
        db.create_unique(u'greenhouse_uploads', ['package', 'version'])

        # Adding model 'People'
        db.create_table(u'greenhouse_people', (
            ('authoritative_person', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['greenhouse.People'], null=True)),
            ('name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('control_group', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exclude', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'greenhouse', ['People'])

        # Deleting model 'Activity'
        db.delete_table(u'greenhouse_activity')

        # Deleting model 'Person'
        db.delete_table(u'greenhouse_person')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'comments.comment': {
            'Meta': {'ordering': "('submit_date',)", 'object_name': 'Comment', 'db_table': "'django_comments'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'content_type_set_for_comment'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_removed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_pk': ('django.db.models.fields.TextField', [], {}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'default': 'None'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment_comments'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'greenhouse.activity': {
            'Meta': {'unique_together': "(('package', 'version'),)", 'object_name': 'Activity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['greenhouse.Person']"}),
            'package': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'null': 'True', 'to': u"orm['greenhouse.Person']"}),
            'subproject': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'version': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'greenhouse.person': {
            'Meta': {'object_name': 'Person'},
            'authoritative_person': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['greenhouse.Person']", 'null': 'True'}),
            'control_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'exclude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'greenhouse.udd': {
            'Meta': {'unique_together': "(('source', 'version'),)", 'object_name': 'UDD', 'db_table': "u'upload_history'", 'managed': 'False'},
            'changed_by': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'changed_by_email': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'changed_by_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'primary_key': 'True'}),
            'distribution': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'file': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fingerprint': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'key_id': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'maintainer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'maintainer_email': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'maintainer_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'nmu': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'signed_by': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'signed_by_email': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'signed_by_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'source': ('django.db.models.fields.TextField', [], {}),
            'version': ('django.db.models.fields.TextField', [], {})
        },
        u'greenhouse.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['greenhouse']