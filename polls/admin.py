from django.contrib import admin
from polls.models import (Survey, Stock, Response)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'date_created', 'start_date', 'end_date', 'stocks', 'n_responses_opened')

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey', 'date_responded')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker')
