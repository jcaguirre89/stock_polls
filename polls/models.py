import json

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.shortcuts import reverse

from users.models import User


class Stock(models.Model):
    ticker = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.ticker

class Survey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')
    date_created = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=300)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    data = JSONField(blank=False, null=True)

    def __str__(self):
        return self.name

    def get_success_url(self):
        """ redirect here after survey is completed """
        return reverse('polls:thankyou', kwargs={'survey_id': self.id})

    @property
    def update_url(self):
        return 'polls:update_survey'

    @property
    def delete_url(self):
        return 'polls:delete_survey'

    @property
    def stocks(self):
        """ Stocks in the current survey """
        tickers = self._stocks_dict2list(self.data)
        stock_objects = [Stock.objects.get(pk=ticker) for ticker in tickers]
        return stock_objects


    @property
    def n_stocks(self):
        """ Number of stocks in survey """
        return len(self.stocks)

    @property
    def n_responses_opened(self):
        """ Number of responses opened """
        if self.responses:
            return len(self.responses.all().open())
        return 0

    @property
    def n_responses_completed(self):
        """ Number of responses completed """
        if self.responses:
            return len(self.responses.all().completed())
        return 0


    @staticmethod
    def _stocks_dict2list(stocks_json):
        """
        turns a dictionary of stocks as it comes from the survey's form to a list of Stock objects
        schema is [{stock: <ticker>}, ..]
        """
        as_dict = json.loads(stocks_json)
        return [item['stock'] for item in as_dict]


class ResponseQuerySet(models.QuerySet):

    def open(self):
        """ Returns list, not QS"""
        return [response for response in self.all() if response.is_open]

    def completed(self):
        """ Returns list, not QS"""
        return [response for response in self.all() if not response.is_open]

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respondents')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    date_responded = models.DateTimeField(default=timezone.now)
    data = JSONField(blank=False, null=True)
    objects = ResponseQuerySet.as_manager()

    def __str__(self):
        return f'Response for {self.survey.name}'

    @property
    def is_open(self):
        if self.data is None:
            return True
        return False