from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('company', 'address', 'state', 'postal_code')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. This will be the username you use to log back in.')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)

