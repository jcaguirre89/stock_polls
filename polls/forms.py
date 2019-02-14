import json

from django import forms

from polls.models import Survey, Response, Stock

class SurveyForm(forms.ModelForm):
    # Additional fields
    stocks = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            required=True, queryset=Stock.Objects.all())


    class Meta:
        model = Survey
        fields = ['name', 'start_date', 'end_date']

    def save(self, commit=True):
        # save as json
        selected_stocks = self.cleaned_data('stocks')
        as_dict = [{'stock': stock} for stock in selected_stocks]
        self.instance.data = json.dumps(as_dict)
        return super().save(commit=commit)

