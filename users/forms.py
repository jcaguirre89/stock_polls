from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, Profile


class SignUpForm(UserCreationForm):
    USER_TYPES = Profile.USER_TYPES

    first_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=100, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. This will be the username you use to log back in.')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        """ Add user type field to form """
        UserCreationForm.__init__(self, *args, **kwargs)
        self.fields['user_type'] = forms.ChoiceField(choices=self.USER_TYPES, initial=Profile.RESPONDENT, required=True,
                                                     help_text='Select whether you want to create or respond surveys',
                                                     label='Surveyor or Respondent')

    def save(self, commit=True):
        """ create profile entry with user type """
        user = super().save(commit=commit)
        # Load profile created in signal just now
        user.refresh_from_db()
        user.profile.user_type = self.cleaned_data['user_type']
        user.profile.save()
        return user
