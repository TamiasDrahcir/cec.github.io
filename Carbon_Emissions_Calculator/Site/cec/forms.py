from django import forms
from .models import Survey, Airport
import datetime

surveys_choice=[]

for i in Survey.objects.all():
    if i.status != "Disabled":
        surveys_choice.append((i.title,i.title))

trans_choice = [
        ("Plane","Plane"),
        ("Train","Train"),
        ("Other","Other"),
        ("None","None")
    ]

cohort_choice = [
        ("FP","FP"),
        ("DP1","DP1"),
        ("DP2","DP2"),
        ("Faculty","Faculty")
    ]

houses = (
    ('Bari', 'Bari'),
    ('Ikhaya', 'Ikhaya'),
    ('Ruka', 'Ruka'),
    ('Meraki', 'Meraki'),
    ('Baile', 'Baile'),
    ('Hogan', 'Hogan'),
    ('Heimat', 'Heimat'),
    ('Bandele', 'Bandele'),
    ('Bayt', 'Bayt'),
    ('Efie', 'Efie'),
    ('Ohana', 'Ohana'),
    ('Other', 'Other'),
)

accounts = {
    ("Resident","Resident"),
    ("Operator","Operator"),
    ("Administrator","Administrator"),
}

class NewPlaneEntry(forms.Form):

    survey = forms.ChoiceField(choices=surveys_choice,required=True)
    cohort = forms.ChoiceField(choices=cohort_choice)    
    identification = forms.CharField(label = "Flight Number (if applicable)",max_length=10,required=False)
    
class NewTrainEntry(forms.Form):

    survey = forms.ChoiceField(choices=surveys_choice)
    cohort = forms.ChoiceField(choices=cohort_choice) 
    identification = forms.CharField(label = "Train Number (if applicable)",max_length=10,required=False)

class NewOtherEntry(forms.Form):

    survey = forms.ChoiceField(choices=surveys_choice)
    cohort = forms.ChoiceField(choices=cohort_choice) 
    identification = forms.CharField(label = "Please provide details on your travel,\nincluding transportation type and departure/destination",max_length=1000,widget=forms.Textarea,required=True)

class NoneSurvey(forms.Form):

    survey = forms.ChoiceField(choices=surveys_choice)
    cohort = forms.ChoiceField(choices=cohort_choice)
    confirm = forms.MultipleChoiceField(choices=(("Yes, I confirm","Yes, I confirm"),("No, take me back","No, take me back")),widget=forms.SelectMultiple(attrs={'size':'2'}))

class ModifyEntry(forms.Form):
    carbon_emissions=forms.FloatField(required=True)

class DeleteEntry(forms.Form):
    confirm=forms.BooleanField(required=True)

class ChangeUserAttributes(forms.Form):
    account=forms.ChoiceField(choices=accounts)

class CarbonCalculator(forms.Form):
    distance=forms.FloatField(required=False)
    type = forms.CharField(max_length=100,required=False)
    emission = forms.FloatField(required=False)
    
class AddSurvey(forms.Form):
    title=forms.CharField(max_length=150)
    opening=forms.DateField(required=True,widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    deadline=forms.DateField(required=True,widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))

class ChangeSurvey(forms.Form):
    opening=forms.DateField(required=True,widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))
    deadline=forms.DateField(required=True,widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}))

class DeleteSurvey(forms.Form):
    confirm=forms.BooleanField(required=True)

class OrganizeEntries(forms.Form):
    surveys_choice.insert(0,("All","All"))
    trans_choice.insert(0,("All","All"))
    survey = forms.ChoiceField(choices=surveys_choice)
    transportation = forms.ChoiceField(choices=trans_choice)
    only_review = forms.BooleanField(required=False)
    category = forms.ChoiceField(choices=(("Time","Time"),("Emissions", "Emissions")))
    order = forms.ChoiceField(choices=(("Ascending","Ascending"),("Descending", "Descending")))