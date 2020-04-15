import random

from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Perform one step in the simulation.
        accounts = request.user.accounts
        tip = ""  # Text to display to the user based on certain events

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
                tip += f"A quarterly dividend from your investments of ${dividend} has been deposited into your bank. "

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
            tip += f"Payday! ${accounts.wage} has been deposited into your bank. "

        accounts.save()
        context = {"accounts": accounts, "tip": tip}
        return render(request, "index.html", context=context)
