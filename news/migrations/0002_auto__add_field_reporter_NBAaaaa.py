# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Reporter.NBAaaaa'
        db.add_column('news_reporter', 'NBAaaaa', self.gf('django.db.models.fields.CharField')(default='aa33s', max_length=70), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Reporter.NBAaaaa'
        db.delete_column('news_reporter', 'NBAaaaa')


    models = {
        'news.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'reporter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.Reporter']"})
        },
        'news.class_a': {
            'Meta': {'object_name': 'Class_A'},
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'munchie'", 'blank': 'True', 'null': 'True', 'to': "orm['news.Class_A']"})
        },
        'news.class_b': {
            'Meta': {'object_name': 'Class_B'},
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ddddd': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.Class_A']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'munchie'", 'blank': 'True', 'null': 'True', 'to': "orm['news.Class_B']"})
        },
        'news.class_c': {
            'Meta': {'object_name': 'Class_C'},
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'munchie'", 'blank': 'True', 'null': 'True', 'to': "orm['news.Class_C']"})
        },
        'news.reporter': {
            'Meta': {'object_name': 'Reporter'},
            'NBA': ('django.db.models.fields.CharField', [], {'default': "'aa33s'", 'max_length': '70'}),
            'NBAaaaa': ('django.db.models.fields.CharField', [], {'default': "'aa33s'", 'max_length': '70'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['news']
