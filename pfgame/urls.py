from django.urls import path
from .views import IndexView, InvestView, DivestView, CCPaymentView, BuyView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("invest/", InvestView.as_view(), name="invest"),
    path("divest/", DivestView.as_view(), name="divest"),
    path("cc/", CCPaymentView.as_view(), name="CCPayment"),
    path("buy/<int:pk>/", BuyView.as_view(), name="buy"),
]
