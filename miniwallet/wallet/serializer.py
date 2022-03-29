from dataclasses import fields
from rest_framework import serializers
from wallet.models import Deposits, Wallet, Withdrawals


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'owned_by', 'status', 'enabled_at', 'balance']

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawals
        exclude = ['owned_by']

class DepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposits
        exclude = ['owned_by']
        