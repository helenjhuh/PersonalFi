from django.db import models
from django.contrib.auth.models import User


class GameProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="accounts")
    week_number = models.IntegerField(default=0, help_text="Set to 0 if new player.")
    bank_balance = models.IntegerField(default=0)
    investment_balance = models.IntegerField("Value of investments", default=0)
    cc_current_month = models.IntegerField(
        "Current month's credit card balance",
        default=0,
        help_text="The portion of credit card balance that does not accrue interest.",
    )
    cc_overdue_balance = models.IntegerField(
        "Overdue credit card balance",
        default=0,
        help_text="The portion of credit card balance that accrues interest.",
    )
    wage = models.IntegerField(
        default=0, help_text="Paid fortnightly, 0 if unemployed."
    )

    @property
    def cc_balance(self):
        return self.cc_current_month + self.cc_overdue_balance


class GameItem(models.Model):
    description = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    owned_by = models.ManyToManyField(User, related_name="items", blank=True)

    def __str__(self):
        return self.description
