import random

from pfgame.forms import InvestForm, DivestForm, CCPaymentForm

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

        # Handle negative balances.
        if accounts.bank_balance < 0:
            OVERDRAFT_FEE = 250
            accounts.bank_balance -= OVERDRAFT_FEE
            tip += f"You've overdrawn your bank account! An overdraft fee of ${OVERDRAFT_FEE} has been charged. Please deposit funds to cover the overdraft.<br/>"
        if accounts.cc_current_month < 0:
            accounts.bank_balance -= (
                accounts.cc_current_month
            )  # Minus negative equivalent to addition
            accounts.cc_current_month = 0
            tip += (
                "A credit from your credit card has been deposited into your bank.<br/>"
            )
        if accounts.cc_overdue_balance < 0:
            accounts.bank_balance -= (
                accounts.cc_overdue_balance
            )  # Minus negative equivalent to addition
            accounts.cc_overdue_balance = 0
            tip += (
                "A credit from your credit card has been deposited into your bank.<br/>"
            )

        # Randomly update investments.
        if accounts.investment_balance:
            investment_multiplier = random.randint(97, 103) / 100
            accounts.investment_balance = max(
                0, round(accounts.investment_balance * investment_multiplier)
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

        if accounts.cc_overdue_balance:
            tip += "Your credit card is past due. Quickly paying a credit account helps avoid interest charges and the deactivation of your card.<br/>"

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
        if form.cleaned_data["amount"] < 0:
            form.cleaned_data["amount"] = 0
        elif form.cleaned_data["amount"] > self.request.user.accounts.bank_balance:
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
        if form.cleaned_data["amount"] < 0:
            form.cleaned_data["amount"] = 0
        elif (
            form.cleaned_data["amount"] > self.request.user.accounts.investment_balance
        ):
            form.cleaned_data["amount"] = self.request.user.accounts.investment_balance
        self.request.user.accounts.investment_balance -= form.cleaned_data["amount"]
        self.request.user.accounts.bank_balance += form.cleaned_data["amount"]
        self.request.user.accounts.save()
        return super().form_valid(form)


class CCPaymentView(FormView):
    template_name = "cc_payment.html"
    form_class = CCPaymentForm
    success_url = "/"

    def form_valid(self, form):
        if form.cleaned_data["amount"] < 0:
            form.cleaned_data["amount"] = 0
        elif form.cleaned_data["amount"] > self.request.user.accounts.bank_balance:
            form.cleaned_data["amount"] = self.request.user.accounts.bank_balance
        elif form.cleaned_data["amount"] > self.request.user.accounts.cc_balance:
            form.cleaned_data["amount"] = self.request.user.accounts.cc_balance
        self.request.user.accounts.cc_overdue_balance -= form.cleaned_data["amount"]
        self.request.user.accounts.bank_balance -= form.cleaned_data["amount"]
        if self.request.user.accounts.cc_overdue_balance < 0:
            # Functionally equivalent to subtraction since value is negative
            self.request.user.accounts.cc_current_month += (
                self.request.user.accounts.cc_overdue_balance
            )
            self.request.user.accounts.cc_overdue_balance = 0
        self.request.user.accounts.save()
        return super().form_valid(form)
