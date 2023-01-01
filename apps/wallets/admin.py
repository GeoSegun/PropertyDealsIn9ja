from django.contrib import admin
from apps.wallets.models import Wallet, WalletTransaction


class WalletAdmin(admin.ModelAdmin):
    readonly_fields = ('uid', 'user', 'currency', 'balance',)
    # list_display_links = ('user', 'id',)
    list_filter = ['currency']
    search_fields = ('user',)


admin.site.register(Wallet, WalletAdmin)


class WalletTransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'wallet', 'currency', 'amount', 'payment_status', 'payment_gateway',)
    # list_display_links = ('wallet',)
    list_filter = ['currency', 'amount', 'payment_status', 'payment_gateway']
    search_fields = ('wallet',)


admin.site.register(WalletTransaction, WalletTransactionAdmin)
