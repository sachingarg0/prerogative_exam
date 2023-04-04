from django import forms
from .models import *
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(label = "Password" , widget=forms.PasswordInput)

class Testform(forms.ModelForm):
    
    class Meta:
        model= Test
        fields = ['name',]
        

        def clean_name(self):
            name = self.cleaned_data['name']
            if Test.objects.filter(name=name).exists():
                raise ValidationError('This name is already taken.')
            return name



class StudentForm(forms.ModelForm):
    dob = forms.DateField(label="Date Of Birth" ,localize=True,widget=forms.DateInput(attrs={'type': 'date','style':'color:grey; font-size:13.5px'}),)
    email = forms.EmailField(required=True, label="Email")
    class Meta:
        model= Student
        fields ="__all__"
        exclude=('test_id','email_token','marks','test_complete')

    def __init__(self, *args, **kwargs):
            super(StudentForm, self).__init__(*args, **kwargs)
            placeholders = {
                'name': 'Enter your name',
                'father_name': "Enter Father's name",                
                'dob': 'DD/MM/YYYY',
                'gender': 'Gender',
                'email' :'Email',
                'phone_number': 'Enter phone number',
                
            }
            for field in self.fields:
                self.fields[field].widget.attrs.update({
                    'placeholder': placeholders.get(field, ''),
                })




