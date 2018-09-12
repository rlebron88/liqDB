from __future__ import unicode_literals
from django.db import models
import django_tables2 as tables
from datetime import datetime
import dateutil.parser

class Study (models.Model):
    SRP = models.CharField(max_length=100)
    PRJ = models.CharField(max_length=100)
    Organism = models.CharField(max_length=100)
    Abstract = models.CharField(max_length=1000)
    Url = models.CharField(max_length=100)
    Title = models.CharField(max_length=100)


class Sample (models.Model):
    SRP = models.CharField(max_length=100)
    PRJ = models.CharField(max_length=100)
    Organism = models.CharField(max_length=100, default="NA")
    Experiment = models.CharField(max_length=100, default ="-")
    Sample = models.CharField(max_length=100)
    Runs = models.CharField(max_length=200)
    Instrument = models.CharField(max_length=100, default="NA")
    Release =  models.CharField(default=2018, max_length=100)
    Sex = models.CharField(max_length=100)
    Fluid = models.CharField(max_length=100)
    Extraction = models.CharField(max_length=100, default="NA")
    Library = models.CharField(max_length=100, default="NA")
    Healthy = models.CharField(max_length=100, default="NA")
    Cancer = models.CharField(max_length=100, default="NA")
    Exosome = models.CharField(max_length=100, default="False")
    Desc = models.CharField(max_length=100, default="False")
    Date = models.DateTimeField( editable = True,default=datetime.now())
    RC = models.IntegerField(default=0)
    #Adapter = models.CharField(max_length=100, default="-")


class StudiesTable(tables.Table):
    class Meta:
        model = Study


def load_RC(input_file):
    with input_file as handle:
        for line in handle:
            exp, rc = line.replace('"', '').replace("'", '').strip().split('\t')
            rc = int(rc)
            Sample.objects.filter(Experiment=exp).update(RC=rc)

# Create your models here.

