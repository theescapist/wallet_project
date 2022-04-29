from django.contrib.auth.models import User
from rest_framework import serializers
from wallets.models import Wallet, Currency


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletRenameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['title']


class WalletDepositSerializer(serializers.Serializer):
    # проверка введенного числа, не допускает использование отрицательных чисел
    amount = serializers.FloatField(min_value=0)


class WalletTransferSerializer(serializers.Serializer):
    # проверка введенного числа, не допускает использование отрицательных чисел
    amount = serializers.FloatField(min_value=0)
    # принимает id кошелька на который совершается перевод
    wallet_to_id = serializers.IntegerField()

    # не дает перевести больше денег чем есть на кошельке
    def validate_amount(self, amount):
        if self.context['wallet_from_amount'] - amount < 0:
             raise serializers.ValidationError("Not enough cash")
        return amount

    # проевряет наличие кошелька с указанным id, если такого нет выдает ошибку
    def validate_wallet_to_id(self, wallet_to_id):
        if not Wallet.objects.filter(pk=wallet_to_id).exists():
            raise serializers.ValidationError("Wallet does not exist")
        return wallet_to_id


class WalletWithdrawSerializer(serializers.Serializer):
    # проверка введенного числа, не допускает использование отрицательных чисел
    amount = serializers.FloatField(min_value=0)

    # не дает перевести больше денег чем есть на кошельке
    def validate_amount(self, amount):
        if self.context['wallet_from_amount'] - amount < 0:
             raise serializers.ValidationError("Not enough cash")
        return amount


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
