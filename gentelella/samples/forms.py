from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Div ,Row
from app.models import Sample
import string
import random
import os
from gentelella.settings import BASE_DIR, DATA_FOLDER, MEDIA_ROOT
from django.db.models import Q


def generate_uniq_id(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


samples = Sample.objects.all()
fluid_list = list(set(samples.values_list('Fluid', flat=True)))
fluid_list.remove("NA")
health_list = list(set(samples.values_list('Healthy', flat=True)))
health_list.remove("NA")
extraction_list = list(set(samples.values_list('Extraction', flat=True)))
sex_list = list(set(samples.values_list('Sex', flat=True)))
library_list = list(set(samples.values_list('Library', flat=True)))


class SamplesForm(forms.Form):
    fluids = [(None, "All")] + [(element, element) for element in sorted(fluid_list, key=str.lower)]
    health_choice = [(None, "All")] + [(element, element) for element in health_list]
    extraction_choice = [(None, "All")] + [(element, element) for element in sorted(extraction_list, key=str.lower)]
    # extraction_choice =
    sex_choice = [(None, "Both")] + [("mf", "Both (only annotated)")] + [(element, element) for element in sex_list]
    # sex_choice = (("", "All"), ("mf", "mf"),("male","male"),("female","female"))
    library_choice = [(None, "All")] + [(element, element) for element in sorted(library_list, key=str.lower)]
    #extraction_choice = [""] + list(set(samples.values_list('Extraction', flat=True)))
    #library_choice = [""] + list(set(samples.values_list('Library', flat=True)))
    #fluids = samples.values_list('Fluid', flat=True)
    fluid =  forms.ChoiceField(label="Fluid",choices=fluids,required=False)
    sex =  forms.ChoiceField(label="Sex",choices=sex_choice,required=False)
    healthy =  forms.ChoiceField(label="Healthy Subjects",choices=health_choice,required=False)
    extraction =  forms.ChoiceField(label="RNA Extraction Protocol",choices=extraction_choice,required=False)
    library =  forms.ChoiceField(label="RNA Library Preparation",choices=library_choice,required=False)

    #field2=  forms.CharField(label=')', required=False)

    ##choices go here
    def __init__(self, *args, **kwargs):
        super(SamplesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('fluid', wrapper_class='col-md-2',css_class='form-control'),
                Field('sex', wrapper_class='col-md-2',css_class='form-control'),
                Field('healthy', wrapper_class='col-md-2',css_class='form-control'),
                Field('extraction', wrapper_class='col-md-2',css_class='form-control'),
                Field('library', wrapper_class='col-md-2',css_class='form-control'),
                ButtonHolder(
                    # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                    Submit('submit', 'FILTER', onclick="$('#loadpage').show(); $('#divPageContent').hide();", css_class='btn btn-primary btn-form')
                    # onsubmit="alert('Neat!'); return false")
                ),
                css_class='form-row')
        )

    def generate_id(self):
        is_new = True
        while is_new:
            query_id = generate_uniq_id()
            #query_path =os.path.join(MEDIA_ROOT,query_id)
            query_path =os.path.join(DATA_FOLDER,"queryData",query_id)
            if not os.path.exists(query_path):
                os.mkdir(query_path)
                return query_id

    def make_query(self,cleaned_data,query_id):

        fluid = str(cleaned_data.get("fluid"))
        sex = str(cleaned_data.get("sex"))
        healthy = str(cleaned_data.get("healthy"))
        extraction = str(cleaned_data.get("extraction"))
        library = str(cleaned_data.get("library"))
        samples = Sample.objects.all()
        #samples = Sample.objects.all()

        #print(samples)

        if fluid:
            fluid_list = [fluid]
        else:
            fluid_list = list(set(samples.values_list('Fluid', flat=True)))
        if sex:
            if sex == "mf":
                sex_list = ["male","female"]
            else:
                sex_list = [sex]
        else:
            sex_list = list(set(samples.values_list('Sex', flat=True)))
        if healthy:
            health_list = [healthy]
        else:
            health_list = list(set(samples.values_list('Healthy', flat=True)))

        if extraction:
            extraction_list=[extraction]
        else:
            extraction_list = list(set(samples.values_list('Extraction', flat=True)))

        if library:
            library_list=[library]
        else:
            library_list = list(set(samples.values_list('Library', flat=True)))

        querySamples = Sample.objects.all().filter(Fluid__in=fluid_list).filter(Sex__in=sex_list).filter(Healthy__in=health_list).filter(Extraction__in=extraction_list).filter(Library__in=library_list).values_list('Experiment', flat=True)

        queryString = ",".join(querySamples)
        #print(len(querySamples))
        #samples_ids = samples.values_list('Experiment',flat=True)
        #print(samples_ids)
        #print(len(samples_ids))

        query_path = os.path.join(DATA_FOLDER,"queryData", query_id)
        outputPath = os.path.join(query_path,"queryOutput")

        call = "java -jar /opt/sRNAtoolboxDB/exec/liqDB.jar output={outputPath} mode=matrix sampleString={sampleString}".format(
            outputPath=outputPath,
            sampleString=queryString
        )


        with open(os.path.join(query_path,"query.txt"), "w") as text_file:
            text_file.write(queryString)
        #print(query_id,fluid,sex,healthy,extraction,library)
        return(query_id,call)
    def start_query(self):
        query_id = self.generate_id()
        return self.make_query(self.cleaned_data,query_id)

class ManualForm(forms.Form):

    hiddenIDs = forms.CharField(label='', required=False, widget=forms.HiddenInput, max_length=2500)

    #field2=  forms.CharField(label=')', required=False)

    ##choices go here
    def __init__(self, *args, **kwargs):
        super(SamplesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field(' hiddenIDs', name=' hiddenIDs'),
                #Field('library', wrapper_class='col-md-2',css_class='form-control'),
                ButtonHolder(
                    # Submit('submit', 'RUN', css_class='btn btn-primary', onclick="alert('Neat!'); return true")
                    Submit('submit', 'KEEP SELECTED', onclick="$('#loadpage').show(); $('#divPageContent').hide();", css_class='btn btn-primary btn-form')
                    # onsubmit="alert('Neat!'); return false")
                ),
                css_class='form-row')
        )

    def generate_id(self):
        is_new = True
        while is_new:
            query_id = generate_uniq_id()
            #query_path =os.path.join(MEDIA_ROOT,query_id)
            query_path =os.path.join(DATA_FOLDER,"queryData",query_id)
            if not os.path.exists(query_path):
                os.mkdir(query_path)
                return query_id

    def make_query(self,cleaned_data,query_id):

        fluid = str(cleaned_data.get("fluid"))
        sex = str(cleaned_data.get("sex"))
        healthy = str(cleaned_data.get("healthy"))
        extraction = str(cleaned_data.get("extraction"))
        library = str(cleaned_data.get("library"))
        samples = Sample.objects.all()
        #samples = Sample.objects.all()

        #print(samples)

        if fluid:
            fluid_list = [fluid]
        else:
            fluid_list = list(set(samples.values_list('Fluid', flat=True)))
        if sex:
            if sex == "mf":
                sex_list = ["male","female"]
            else:
                sex_list = [sex]
        else:
            sex_list = list(set(samples.values_list('Sex', flat=True)))
        if healthy:
            health_list = [healthy]
        else:
            health_list = list(set(samples.values_list('Healthy', flat=True)))

        if extraction:
            extraction_list=[extraction]
        else:
            extraction_list = list(set(samples.values_list('Extraction', flat=True)))

        if library:
            library_list=[library]
        else:
            library_list = list(set(samples.values_list('Library', flat=True)))

        querySamples = Sample.objects.all().filter(Fluid__in=fluid_list).filter(Sex__in=sex_list).filter(Healthy__in=health_list).filter(Extraction__in=extraction_list).filter(Library__in=library_list).values_list('Experiment', flat=True)

        queryString = ",".join(querySamples)
        #print(len(querySamples))
        #samples_ids = samples.values_list('Experiment',flat=True)
        #print(samples_ids)
        #print(len(samples_ids))

        query_path = os.path.join(DATA_FOLDER,"queryData", query_id)
        outputPath = os.path.join(query_path,"queryOutput")

        call = "java -jar /opt/sRNAtoolboxDB/exec/liqDB.jar output={outputPath} mode=matrix sampleString={sampleString}".format(
            outputPath=outputPath,
            sampleString=queryString
        )


        with open(os.path.join(query_path,"query.txt"), "w") as text_file:
            text_file.write(queryString)
        #print(query_id,fluid,sex,healthy,extraction,library)
        return(query_id,call)
    def start_query(self):
        query_id = self.generate_id()
        return self.make_query(self.cleaned_data,query_id)