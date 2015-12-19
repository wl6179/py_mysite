# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Reporter'
        db.create_table('news_reporter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('NBA', self.gf('django.db.models.fields.CharField')(max_length=70)),
        ))
        db.send_create_signal('news', ['Reporter'])

        # Adding model 'Article'
        db.create_table('news_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('reporter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['news.Reporter'])),
        ))
        db.send_create_signal('news', ['Article'])

        # Adding model 'Class_A'
        db.create_table('news_class_a', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='munchie', blank=True, null=True, to=orm['news.Class_A'])),
        ))
        db.send_create_signal('news', ['Class_A'])

        # Adding model 'Class_B'
        db.create_table('news_class_b', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='munchie', blank=True, null=True, to=orm['news.Class_B'])),
            ('ddddd', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['news.Class_A'], null=True, blank=True)),
        ))
        db.send_create_signal('news', ['Class_B'])

        # Adding model 'Class_C'
        db.create_table('news_class_c', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='munchie', blank=True, null=True, to=orm['news.Class_C'])),
        ))
        db.send_create_signal('news', ['Class_C'])


    def backwards(self, orm):
        
        # Deleting model 'Reporter'
        db.delete_table('news_reporter')

        # Deleting model 'Article'
        db.delete_table('news_article')

        # Deleting model 'Class_A'
        db.delete_table('news_class_a')

        # Deleting model 'Class_B'
        db.delete_table('news_class_b')

        # Deleting model 'Class_C'
        db.delete_table('news_class_c')


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
            'NBA': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['news']
