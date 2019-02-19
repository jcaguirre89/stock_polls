import json

from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField
from django.shortcuts import reverse
import numpy as np


class Product(models.Model):
    """ Products are uniquely named for each user that created them """
    name = models.CharField(max_length=100, help_text='Short name for this product/service')
    description = models.TextField(blank=True, help_text="Product/service description")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='products')

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return self.slug

    @property
    def slug(self):
        return '-'.join(self.name.strip().lower().split())

    @property
    def update_url(self):
        return 'polls:update_product'

    @property
    def delete_url(self):
        return 'polls:delete_product'

class Survey(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='surveys')
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
    def products(self):
        """ Products in the current survey """
        as_dict = json.loads(self.data)
        ids = [item['id'] for item in as_dict]
        product_objects = [Product.objects.get(pk=product_id) for product_id in ids]
        return product_objects

    def _product_prices(self, product):
        """ Return a list of prices of a product in a survey """
        responses = self.responses.all().completed()
        prices = [response.response_prices[product] for response in responses]
        return prices


    def avg_price_product(self, product):
        """ Average price for a product among respondents """
        if self.n_responses_completed < 1:
            return
        return np.mean(self._product_prices(product))

    @property
    def n_products(self):
        """ Number of products in survey """
        return len(self.products)

    @property
    def n_responses_opened(self):
        """ Number of responses opened """
        qs = self.responses.all()
        if qs:
            return len(qs.open())
        return 0

    @property
    def n_responses_completed(self):
        """ Number of responses completed """
        qs = self.responses.all()
        if qs:
            return len(qs.completed())
        return 0


class ResponseQuerySet(models.QuerySet):

    def open(self):
        """ Returns list, not QS"""
        return [response for response in self.all() if response.is_open]

    def completed(self):
        """ Returns list, not QS"""
        return [response for response in self.all() if not response.is_open]

class Response(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='respondents')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    date_responded = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)
    data = JSONField(blank=False, null=True)
    objects = ResponseQuerySet.as_manager()

    def __str__(self):
        return f'Response for {self.survey.name}'

    def get_absolute_url(self):
        return reverse('polls:response_detail', kwargs={'pk': self.id})

    @property
    def is_open(self):
        if self.data is None:
            return True
        return False

    @property
    def is_complete(self):
        if self.data is not None:
            return True
        return False

    @property
    def clean_data(self):
        """
        returns products and prices in response as a dict
        products are Product objects
        schema comes as {<name>: price, <name>: price, ...}
        returns {Product: price, Product: price, ...}
        """
        if self.is_open:
            return
        # data is stored as a json list of dictionaries
        data = json.loads(self.data)
        out_data = {
            Product.objects.get(name=name, user=self.survey.user): price
            for name, price in data.items()
            }
        return out_data

    @property
    def prices(self):
        """ Return list of prices in response """
        return list(self.clean_data.values())

    def bid_price(self, product):
        """ Return a product's price given by the respondent for a given Product object """
        return self.clean_data[product]

