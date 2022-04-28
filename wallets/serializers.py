from django.contrib.auth.models import User, Group
from rest_framework import serializers
from wallets.models import Wallet, Currency



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletRenameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['title']


class WalletDepositSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['amount'] < 0.01:
            raise serializers.ValidationError("Deposit amount can't be less than 0.01")
        return data

    class Meta:
        model = Wallet
        fields = ['amount']


class WalletTransferSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=0)
    wallet_to_id = serializers.IntegerField()

    def validate_amount(self, amount):
        if self.context['wallet_from_amount'] - amount < 0:
             raise serializers.ValidationError("Not enough cash")
        return amount

    def validate_wallet_to_id(self, wallet_to_id):
        if not Wallet.objects.filter(pk=wallet_to_id).exists():
            raise serializers.ValidationError("Wallet does not exist")
        return wallet_to_id


class WalletWithdrawSerializer(serializers.ModelSerializer):
    def validate(self, data):
        if data['amount'] < 0.01:
            raise serializers.ValidationError("Withdraw amount can't be less than 0.01")
    class Meta:
        model = Wallet
        fields = ['amount']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

