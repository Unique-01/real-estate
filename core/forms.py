from django import forms
from .models import *
from registration.forms import *
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_image', 'contact_info', 'about']
        widgets = {
            'profile_image': forms.FileInput(attrs={'onchange': "PreviewImage();"})
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]


class CustomRegistrationForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService, RegistrationFormUsernameLowercase):
    first_name = forms.CharField(
        max_length=30, required=True)
    last_name = forms.CharField(
        max_length=30, required=True)


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # fields = '__all__'
        widgets = {
            'year_of_construction': forms.DateInput(attrs={'type': 'date'}),
            'last_renovation': forms.DateInput(attrs={'type': 'date'})
        }
        fields = ['country', 'region', 'city', 'title', 'description', 'price', 'property_type', 'category', 'address', 'property_type',
                  'area_size', 'bedroom', 'bathroom', 'garage', 'room', 'postal_code', 'year_of_construction', 'last_renovation']
