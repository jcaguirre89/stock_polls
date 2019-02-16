

from django.views.generic import FormView, TemplateView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect, render
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy


from users.forms import SignUpForm, ProfileForm

from users.models import User, Profile

# Create your views here.

class SignUp(FormView):
    template_name = 'registration/signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('polls:survey_list')

    def form_valid(self, form):
        """ Save and redirect to corresponding site """
        user = form.save()
        # Log the user in
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=user.email, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)

class Index(TemplateView):
    template_name = 'users/index.html'

class UpdateProfile(FormView):
    form_class = ProfileForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('polls:survey_list')

