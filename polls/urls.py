from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.ListSurvey.as_view(), name='survey_list'),
    # Survey CRUD
    path('ajax/create_survey/', views.CreateSurvey.as_view(), name='create_survey'),
    path('ajax/update_survey/<int:pk>/', views.UpdateSurvey.as_view(), name='update_survey'),
    path('ajax/delete_survey/<int:pk>/', views.DeleteSurvey.as_view(), name='delete_survey'),

    path('survey/choose-survey/', views.ChooseSurvey.as_view(), name='choose_survey'),
    path('survey/<int:survey_id>/respond/', views.respond_survey, name='respond_survey'),
    path('survey/<int:survey_id>/thankyou/', views.thankyou, name='thankyou'),

    # Responses
    path('survey/<int:survey_id>/responses/', views.ResponseList.as_view(), name='response_list'),
    path('survey/<int:pk>/response-detail/', views.ResponseDetail.as_view(), name='response_detail'),

    # Product CRUD
    path('products/', views.ListProduct.as_view(), name='product_list'),
    path('ajax/create_product/', views.CreateProduct.as_view(), name='create_product'),
    path('ajax/update_product/<int:pk>/', views.UpdateProduct.as_view(), name='update_product'),
    path('ajax/delete_product/<int:pk>/', views.DeleteProduct.as_view(), name='delete_product'),

]