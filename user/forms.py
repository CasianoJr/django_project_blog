from django import forms
from .models import Profile, Bio
from django.forms import inlineformset_factory

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'address', 'contact', 'headshot',]

BioFormSet = inlineformset_factory(Profile, Bio, 
    fields=('field', 'field_description',),
    widgets={'field_description': forms.Textarea(attrs={'rows': 3})}, 
    extra=3, max_num=15, can_delete=True)