from django.shortcuts import render
from django.views.generic import CreateView

def survey_list(request):
    return render(request, 'polls/survey_list.html')