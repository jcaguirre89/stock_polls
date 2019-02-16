

from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect, render
from django.contrib.auth import login, authenticate

from users.forms import SignUpForm

from users.models import User, Profile

# Create your views here.

class SignUp(FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm

    def form_valid(self, form):
        """ Save and redirect to corresponding site """
        user = form.save()
        # Log the user in
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=user.email, password=raw_password)
        login(self.request, user)

        if form.cleaned_data['user_type'] == Profile.SURVEYOR:
            return HttpResponseRedirect(reverse('polls:survey_list'))
        else:
            return HttpResponseRedirect(reverse('polls:choose_survey'))

class Index(TemplateView):
    template_name = 'users/index.html'

