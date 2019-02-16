import json

from django import forms

from polls.models import Survey, Response, Stock

class SurveyForm(forms.ModelForm):
    # Additional fields
    stocks = forms.ModelMultipleChoiceField(required=True, queryset=Stock.objects.all())


    class Meta:
        model = Survey
        fields = ['name', 'start_date', 'end_date']

    def save(self, commit=True):
        # save as json
        selected_stocks = self.cleaned_data.get('stocks')
        as_dict = [{'stock': stock.ticker} for stock in selected_stocks]
        self.instance.data = json.dumps(as_dict)
        return super().save(commit=commit)


class ResponseForm(forms.Form):
    """ Additional args to give form:
    - Response instance
    """

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        self.instance = instance
        stocks = self.instance.survey.stocks
        super().__init__(*args, **kwargs)
        for stock in stocks:
            self.fields[stock.name] = forms.DecimalField()


    def save(self):
        """
        save Response object
        receives the form fields as a dict {'<ticker1>': price1, <ticker2>" price2, ...}
        """
        clean_data = {ticker: float(price) for ticker, price in self.cleaned_data.items()}
        data = json.dumps(clean_data)
        self.instance.data = data
        self.instance.save()


