from django import forms


class InvestForm(forms.Form):
    amount = forms.IntegerField()


class DivestForm(forms.Form):
    amount = forms.IntegerField()


class CCPaymentForm(forms.Form):
    amount = forms.IntegerField()


class BuyForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=(("cash", "Bank balance"), ("cc", "Credit card"))
    )
