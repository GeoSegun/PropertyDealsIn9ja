from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from propertyDealsIn9ja.flutterwave import FLUTTERWAVE_PUBLIC_KEY
from apps.accounts.models import User
from apps.wallets.models import Wallet, WalletTransaction


class WalletTransactionListView(LoginRequiredMixin, View):
    template_name = "wallets/wallet_transactions.html"

    def get(self, request):
        wallet = Wallet.objects.get(user=self.request.user)
        wallet_transactions = wallet.wallet_transactions.all()
        context = {
            'wallet_transactions': wallet_transactions,
        }
        return render(request, self.template_name, context)


class FundWalletView(LoginRequiredMixin, DetailView):
    model = Wallet
    template_name = "wallets/fund_wallet.html"
    context_object_name = "wallet"

    def get_object(self, queryset=None):
        return Wallet.objects.get(uid=self.request.user.wallet.uid)

    def get_context_data(self, **kwargs):
        context = super(FundWalletView, self).get_context_data(**kwargs)
        context["wallet_transactions"] = self.get_object().wallet_transactions.all()
        context["pub_key"] = FLUTTERWAVE_PUBLIC_KEY
        context["get_user"] = User.objects.get(username=self.request.user.username)
        return context


def confirm_fund_view(request, uid):
    wallet = get_object_or_404(Wallet, uid=uid)
    get_currency = request.POST.get('currency')
    get_tx_ref = request.POST.get('tx_ref')
    get_amount = request.POST.get('amount')
    get_status = request.POST.get('status')

    print(f"Your currency => {get_currency}")

    # Update user wallet transaction
    wallet_transaction = WalletTransaction.objects.create(
        wallet=wallet,
        transaction_id=get_tx_ref,
        currency=get_currency,
        amount=get_amount,
        payment_status=get_status,
    )
    wallet.wallet_transactions.add(wallet_transaction)
    print("Wallet transactions updated")

    # Update wallet balance...
    wallet.balance = F('balance') + float(get_amount)
    wallet.save()
    print("Wallet Balance Updated")

    # list wallet transactions...
    wallet_transactions = wallet.wallet_transactions.all()

    context = {
        'wallet_transactions': wallet_transactions,
    }
    messages.success(request, "Fund updated!.")
    return redirect("wallets:fund_wallet", wallet.uid)
