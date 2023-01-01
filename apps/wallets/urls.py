from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from apps.wallets.views import FundWalletView, WalletTransactionListView, confirm_fund_view

urlpatterns = [
    # path('validate_bvn/', csrf_exempt(ValidateBVN.as_view()), name='validate_bvn'),
    # path('<slug:id>/fund_success/', csrf_exempt(ConfirmFundView.as_view()), name='fund_success'),
    path('wallet_transactions/', WalletTransactionListView.as_view(), name='wallet_transactions'),
    path('<slug:uid>/', FundWalletView.as_view(), name='fund_wallet'),
    path('<slug:uid>/fund_success/', confirm_fund_view, name='fund_success'),
]
