from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.ListSurvey.as_view(), name='survey_list'),
    path('ajax/create_survey/', views.CreateSurvey.as_view(), name='create_survey'),
    path('ajax/update_survey/<int:pk>/', views.UpdateSurvey.as_view(), name='update_survey'),
    path('ajax/delete_survey/<int:pk>/', views.DeleteSurvey.as_view(), name='delete_survey'),

    #path('survey/<int:survey_id>/create-response/', views.create_response, name='create_response'),
    path('survey/<int:survey_id>/respond/', views.respond_survey, name='respond_survey'),
    path('survey/<int:survey_id>/thankyou/', views.thankyou, name='thankyou'),
    ]