from django.contrib import admin
from polls.models import (Survey, Product, Response)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'date_created', 'start_date', 'end_date', 'products', 'n_responses_opened')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey', 'date_responded')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', )
