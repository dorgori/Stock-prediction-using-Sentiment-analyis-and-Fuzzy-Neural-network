from django import forms

class StockForm(forms.Form):
    class Meta:
        fields = ['symbol', 'date']