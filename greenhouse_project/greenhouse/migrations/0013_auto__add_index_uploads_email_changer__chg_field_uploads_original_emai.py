# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'People', fields ['email']
        db.delete_unique(u'people', ['email'])

        # Adding index on 'Uploads', fields ['email_changer']
        db.create_index(u'uploads', ['email_changer'])


        # Changing field 'Uploads.original_email_changer'
        db.alter_column(u'uploads', 'original_email_changer', self.gf('django.db.models.fields.EmailField')(default='', max_length=75))
        # Adding field 'People.authoritative'
        db.add_column(u'people', 'authoritative',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


        # Changing field 'People.original_email'
        db.alter_column(u'people', 'original_email', self.gf('django.db.models.fields.EmailField')(default='default', unique=True, max_length=75))
        # Adding unique constraint on 'People', fields ['original_email']
        db.create_unique(u'people', ['original_email'])

        # Adding index on 'People', fields ['email']
        db.create_index(u'people', ['email'])


    def backwards(self, orm):
        # Removing index on 'People', fields ['email']
        db.delete_index(u'people', ['email'])

        # Removing unique constraint on 'People', fields ['original_email']
        db.delete_unique(u'people', ['original_email'])

        # Removing index on 'Uploads', fields ['email_changer']
        db.delete_index(u'uploads', ['email_changer'])


        # Changing field 'Uploads.original_email_changer'
        db.alter_column(u'uploads', 'original_email_changer', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))
        # Deleting field 'People.authoritative'
        db.delete_column(u'people', 'authoritative')


        # Changing field 'People.original_email'
        db.alter_column(u'people', 'original_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))
        # Adding unique constraint on 'People', fields ['email']
        db.create_unique(u'people', ['email'])


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
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'uploads.people': {
            'Meta': {'object_name': 'People', 'db_table': "u'people'"},
            'authoritative': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'contacted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'control_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'db_index': 'True'}),
            'first_upload': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['uploads.Uploads']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_upload': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['uploads.Uploads']"}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'total_uploads': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'ubuntu_dev': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'uploads.udd': {
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
        u'uploads.uploads': {
            'Meta': {'unique_together': "(('package', 'version'),)", 'object_name': 'Uploads', 'db_table': "u'uploads'"},
            'email_changer': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'max_length': '75', 'blank': 'True'}),
            'email_sponsor': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_changer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name_sponsor': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_email_changer': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'package': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'release': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'uploads.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['uploads']