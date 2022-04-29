from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from wallets.permissions import IsOwner
from wallets.serializers import *


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WalletListView(generics.ListCreateAPIView):
    permission_classes = [IsOwner, IsAdminUser]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwner, IsAdminUser]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletRenameView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwner, IsAdminUser]
    queryset = Wallet.objects.all()
    serializer_class = WalletRenameSerializer


class WalletDepositView(APIView):
    permission_classes = [IsOwner, IsAdminUser]

    # формируем PUT запрос
    def put(self, request, pk):
        data = request.data
        wallet = get_object_or_404(Wallet, id=pk)
        amount = data['amount']
        serializer = WalletDepositSerializer(wallet, data=data)
        # проверяем данные в сериализаторе и производим транзакцию
        if serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    wallet.amount += amount
                    wallet.save()
            except Exception as e:
                return Response({"error": f"Transaction failed: {str(e)}"}, status=500)
            return Response({"message": "Transaction success"})


class WalletTransferView(APIView):
    permission_classes = [IsOwner, IsAdminUser]

    # формируем PUT запрос
    def put(self, request, pk):
        data = request.data
        wallet_from = get_object_or_404(Wallet, id=pk)
        # передаем в сериализатор контекст, для проверки хватит ли на кошельке денег для трансфера и проверяем данные
        serializer = WalletTransferSerializer(Wallet, data=data, context={"wallet_from_amount" : wallet_from.amount})
        serializer.is_valid(raise_exception=True)

        wallet_to = Wallet.objects.get(pk=data['wallet_to_id'])
        amount = data['amount']
        ratio = 1
        # запрашиваем коды валют и если они разные, изменяем коэффициент перевода(ratio)
        currency_from = Currency.objects.get(pk=wallet_from.currency.id)
        currency_to = Currency.objects.get(pk=wallet_to.currency.id)
        if currency_from.code != currency_to.code:
            ratio = currency_from.ratio / currency_to.ratio
        # производим транзакцию с конвертацией
        try:
            with transaction.atomic():
                wallet_from.amount -= amount
                wallet_to.amount += amount * ratio
                wallet_to.save()
                wallet_from.save()
        except Exception as e:
            return Response({"error": f"Transaction failed: {str(e)}"}, status=500)
        return Response({"message": "Transaction success"})


class WalletWithdrawView(APIView):
    permission_classes = [IsOwner, IsAdminUser]

    # формируем PUT запрос
    def put(self, request, pk):
        data = request.data
        wallet = get_object_or_404(Wallet, id=pk)
        serializer = WalletWithdrawSerializer(Wallet,  context={"wallet_amount" : wallet.amount})

        amount = data['amount']
        # проверяем данные в сериализаторе и производим транзакцию
        if serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    wallet.amount -= amount
                    wallet.save()
            except Exception as e:
                return Response({"error": f"Transaction failed: {str(e)}"}, status=500)
            return Response({"message": "Transaction success"})


class WalletDeleteView(generics.DestroyAPIView):
    permission_classes = [IsOwner, IsAdminUser]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class CurrenciesView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrenciesDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    