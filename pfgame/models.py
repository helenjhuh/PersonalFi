from django.db import models
from django.contrib.auth.models import User


class GameProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    week_number = models.IntegerField(default=0, help_text="Set to 0 if new player.")
    bank_balance = models.IntegerField(default=0)
    investment_balance = models.IntegerField("Value of investments", default=0)
    property_balance = models.IntegerField("Value of property", default=0)
    cc_balance = models.IntegerField("Credit card balance", default=0, help_text="The portion of credit card balance that does not accrue interest.")
    cc_overdue_balance = models.IntegerField("Overdue credit card balance", default=0, help_text="The portion of credit card balance that accrues interest.")
    mortgage_balance = models.IntegerField(default=0)
    wage = models.IntegerField(
        default=0, help_text="Paid fortnightly, 0 if unemployed."
    )
