from django.urls import path
from wallet import views

urlpatterns = [
    path('api/v1/wallet', views.wallet_list),
    path('api/v1/wallet/deposits', views.deposit),
    path('api/v1/wallet/withdrawals', views.withdrawl),
]