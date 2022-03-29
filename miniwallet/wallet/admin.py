from django.contrib import admin

from wallet.models import Wallet

# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    pass
admin.site.register(Wallet, WalletAdmin)