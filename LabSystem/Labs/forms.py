from django import forms
from django.forms import fields, widgets
from .models import *

class RegisterTester(forms.ModelForm):
    class Meta:
        model = Tester
        fields = '__all__'


class RegisterPatient(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class RegisterSample(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = '__all__'

        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control form-control-select2', 'required':'True','name':'patient', 'placeholder': 'patient'}),
        }

class RegisterVaccination(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = '__all__'

        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control form-control-select2', 'required':'True','name':'patient', 'placeholder': 'patient'}),
        }

class UserLogForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LabCenterForm(forms.ModelForm):
    class Meta:
        model = LabCenter
        fields = '__all__'