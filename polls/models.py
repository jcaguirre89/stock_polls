from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

from users.models import User


class Stock(models.Model):
    name = models.CharField(max_length=300)
    ticker = models.CharField(max_length=20)


class Survey(models.Model):
    survey_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=300)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(defualt=timezone.now)
    data = JSONField()


class Response(models.Model):
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    date_responded = models.DateTimeField(default=timezone.now)
    data = JSONField()

