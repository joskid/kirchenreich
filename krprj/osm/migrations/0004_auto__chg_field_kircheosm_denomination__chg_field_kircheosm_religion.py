# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'KircheOsm.denomination'
        db.alter_column('osm_kircheosm', 'denomination', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'KircheOsm.religion'
        db.alter_column('osm_kircheosm', 'religion', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):

        # Changing field 'KircheOsm.denomination'
        db.alter_column('osm_kircheosm', 'denomination', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'KircheOsm.religion'
        db.alter_column('osm_kircheosm', 'religion', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    models = {
        'osm.kircheosm': {
            'Meta': {'object_name': 'KircheOsm'},
            'addional_fields': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'denomination': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'osm_id': ('django.db.models.fields.IntegerField', [], {}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['osm']