from django import forms


class InvestForm(forms.Form):
    amount = forms.IntegerField()


class DivestForm(forms.Form):
    amount = forms.IntegerField()
