import json

from django import forms

from polls.models import Survey, Response, Product


class SurveyForm(forms.ModelForm):
    # Additional fields

    class Meta:
        model = Survey
        fields = ['name', 'start_date', 'end_date']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['products'] = forms.ModelMultipleChoiceField(required=True,
                                                                 queryset=user.products.all())

    def save(self, commit=True):
        # save as json
        selected_products = self.cleaned_data.get('products')
        as_dict = [{'product': product.slug, 'id': product.id} for product in selected_products]
        self.instance.data = json.dumps(as_dict)
        return super().save(commit=commit)


class ResponseForm(forms.Form):
    """ Additional args to give form:
    - Response instance
    """

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        self.instance = instance
        products = self.instance.survey.products
        super().__init__(*args, **kwargs)
        for product in products:
            self.fields[product.name] = forms.DecimalField(required=False)
        self.fields['comment'] = forms.CharField(widget=forms.Textarea,
                                                 required=False,
                                                 help_text="Leave a comment for the person who created this survey to explain your pricing")


    def save(self):
        """
        save Response object
        Removes comment from form, then save remaining fields as price data
        receives the form fields as a dict {'<name1>': price1, <name2>" price2, ...}

        save as json, schema: [{'name':<name>, 'id': <id>, 'price': <price>}, {...}]
        dont save ID? if name is unique by user, it's not necesary to retrieve from Product model later
        """
        form_data = self.cleaned_data
        comment = form_data.pop('comment', None)
        price_data = [
            {
                'name': name,
                'price': None if price is None else float(price)
             }
            for name, price in form_data.items()
        ]
        data = json.dumps(price_data)
        self.instance.data = data
        self.instance.comment = comment
        self.instance.save()


