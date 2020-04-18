import random

from pfgame.forms import InvestForm, DivestForm

from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Perform one step in the simulation.
        accounts = request.user.accounts
        tip = ""  # Text to display to the user based on certain events, leave a <br/> at the end of each tip when you append to the string.

        # Initialize state for new users.
        if not accounts.week_number:
            if not accounts.wage:
                accounts.wage = random.randint(600, 2000)
                accounts.wage -= accounts.wage % 100  # Round to nearest hundred
            SIGNING_BONUS = 600
            tip += f'Welcome to PersonalFi! You\'ve started a new job, which pays ${accounts.wage} fortnightly. A signing bonus of ${SIGNING_BONUS} has been deposited into your bank (<a href="https://en.wikipedia.org/wiki/Signing_bonus">learn more</a>).<br/>'
            accounts.bank_balance += SIGNING_BONUS

        accounts.week_number += 1

        # Randomly update investments.
        if accounts.investment_balance:
            investment_multiplier = random.randint(97, 103) / 100
            accounts.investment_balance = round(
                accounts.investment_balance * investment_multiplier
            )
            if accounts.week_number % 12 == 0:  # Quarterly
                dividend_yield = random.randint(2, 4) / 100
                dividend = round(accounts.investment_balance * dividend_yield)
                accounts.bank_balance += dividend
                tip += f'A quarterly dividend from your investments of ${dividend} has been deposited into your bank (<a href="https://www.investopedia.com/terms/d/dividend.asp">learn more</a>).<br/>'

        # roll over credit card balances and charge interest
        if accounts.week_number % 4 == 0:  # Monthly
            if accounts.cc_current_month:
                accounts.cc_overdue_balance += accounts.cc_current_month
                accounts.cc_current_month = 0
            interest_multiplier = random.randint(115, 125) / 100
            accounts.cc_overdue_balance = round(
                accounts.cc_overdue_balance * interest_multiplier
            )

        if accounts.wage and accounts.week_number % 2 == 0:  # Fortnightly
            accounts.bank_balance += accounts.wage
            tip += f'Payday! ${accounts.wage} has been deposited into your bank. <a href="https://i.imgur.com/lSoUQr2.png">Spend it wisely!</a><br/>'

        accounts.save()
        context = {"accounts": accounts, "tip": tip}
        return render(request, "index.html", context=context)


class InvestView(FormView):
    template_name = "invest.html"
    form_class = InvestForm
    success_url = "/"

    def form_valid(self, form):
        if form.cleaned_data["amount"] > self.request.user.accounts.bank_balance:
            form.cleaned_data["amount"] = self.request.user.accounts.bank_balance
        self.request.user.accounts.bank_balance -= form.cleaned_data["amount"]
        self.request.user.accounts.investment_balance += form.cleaned_data["amount"]
        self.request.user.accounts.save()
        return super().form_valid(form)


class DivestView(FormView):
    template_name = "divest.html"
    form_class = DivestForm
    success_url = "/"

    def form_valid(self, form):
        if form.cleaned_data["amount"] > self.request.user.accounts.investment_balance:
            form.cleaned_data["amount"] = self.request.user.accounts.investment_balance
        self.request.user.accounts.investment_balance -= form.cleaned_data["amount"]
        self.request.user.accounts.bank_balance += form.cleaned_data["amount"]
        self.request.user.accounts.save()
        return super().form_valid(form)
