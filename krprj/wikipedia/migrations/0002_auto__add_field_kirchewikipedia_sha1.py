# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'KircheWikipedia.sha1'
        db.add_column('wikipedia_kirchewikipedia', 'sha1',
                      self.gf('django.db.models.fields.TextField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'KircheWikipedia.sha1'
        db.delete_column('wikipedia_kirchewikipedia', 'sha1')


    models = {
        'wikipedia.categorywikipedia': {
            'Meta': {'object_name': 'CategoryWikipedia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'wikipedia.kirchewikipedia': {
            'Meta': {'object_name': 'KircheWikipedia'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'categories+'", 'symmetrical': 'False', 'to': "orm['wikipedia.CategoryWikipedia']"}),
            'contents': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infobox': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'languages+'", 'symmetrical': 'False', 'to': "orm['wikipedia.LanguageWikipedia']"}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sha1': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'values': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'values+'", 'symmetrical': 'False', 'to': "orm['wikipedia.ValueStore']"})
        },
        'wikipedia.languagewikipedia': {
            'Meta': {'object_name': 'LanguageWikipedia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'wikipedia.valuestore': {
            'Meta': {'object_name': 'ValueStore'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'default': "''"})
        }
    }

    complete_apps = ['wikipedia']