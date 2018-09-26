from __future__ import unicode_literals
from django.db import models
import django_tables2 as tables
from datetime import datetime
import dateutil.parser

from plotly.offline import plot
import plotly.plotly as py
import plotly.graph_objs as go
import plotly

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
    with open(input_file) as handle:
        for line in handle:
            exp, rc = line.replace('"', '').replace("'", '').strip().split('\t')
            rc = int(rc)
            Sample.objects.filter(Experiment=exp).update(RC=rc)


def fluid_boxplot():
    kind_of_fluids = set(Sample.objects.order_by('Fluid').values_list('Fluid', flat=True))
    rc_by_fluid = {fluid : list(Sample.objects.filter(Fluid=fluid).order_by('RC').values_list('RC', flat=True)) for fluid in kind_of_fluids}
    data = []
    color_list = ["red", "green", "blue", "yellow", "purple", "orange"] * 10
    color_fluid = list(zip(color_list, kind_of_fluids))
    for color, fluid in color_fluid:
        trace = go.Box(
            y = rc_by_fluid[fluid],
            name = fluid,
            marker = dict(
                color = color
            )
        )
        data.append(trace)
    layout = go.Layout(
        autosize=True,
        margin=go.Margin(
            l=50,
            r=50,
            b=150,
            t=100,
            pad=4
        ),
        title="Total Read Counts by Fluid",
        xaxis=dict(
            tickfont=dict(
                size=18
            )
        ),
        yaxis=dict(
            type='log',
            title='Total Read Count'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    div_obj = plot(fig, show_link=False, auto_open=False, output_type = 'div')
    return div_obj
