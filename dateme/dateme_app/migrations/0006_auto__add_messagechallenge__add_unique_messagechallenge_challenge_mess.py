# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MessageChallenge'
        db.create_table(u'dateme_app_messagechallenge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Challenge'])),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dateme_app.Message'])),
            ('picture', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('isComplete', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'dateme_app', ['MessageChallenge'])

        # Adding unique constraint on 'MessageChallenge', fields ['challenge', 'message']
        db.create_unique(u'dateme_app_messagechallenge', ['challenge_id', 'message_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'MessageChallenge', fields ['challenge', 'message']
        db.delete_unique(u'dateme_app_messagechallenge', ['challenge_id', 'message_id'])

        # Deleting model 'MessageChallenge'
        db.delete_table(u'dateme_app_messagechallenge')


    models = {
        u'dateme_app.challenge': {
            'Meta': {'object_name': 'Challenge'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dateme_app.contenttype': {
            'Meta': {'object_name': 'ContentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'dateme_app.conversation': {
            'Meta': {'object_name': 'Conversation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dateme_app.Person']", 'symmetrical': 'False'})
        },
        u'dateme_app.gender': {
            'Meta': {'object_name': 'Gender'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        },
        u'dateme_app.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude_degrees': ('django.db.models.fields.IntegerField', [], {}),
            'latitude_minutes': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '10'}),
            'longitude_degrees': ('django.db.models.fields.IntegerField', [], {}),
            'longitude_minutes': ('django.db.models.fields.DecimalField', [], {'max_digits': '19', 'decimal_places': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"})
        },
        u'dateme_app.message': {
            'Meta': {'object_name': 'Message'},
            'contentType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.ContentType']"}),
            'conversation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Conversation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'dateme_app.messagechallenge': {
            'Meta': {'unique_together': "(('challenge', 'message'),)", 'object_name': 'MessageChallenge'},
            'challenge': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Challenge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isComplete': ('django.db.models.fields.BooleanField', [], {}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Message']"}),
            'picture': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'dateme_app.person': {
            'Meta': {'object_name': 'Person'},
            'age_end': ('django.db.models.fields.IntegerField', [], {}),
            'age_start': ('django.db.models.fields.IntegerField', [], {}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {}),
            'gender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gender'", 'to': u"orm['dateme_app.Gender']"}),
            'handle': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orientation': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'orientation'", 'symmetrical': 'False', 'to': u"orm['dateme_app.Gender']"}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'dateme_app.setting': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('user', 'name'),)", 'object_name': 'Setting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dateme_app.Person']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['dateme_app']