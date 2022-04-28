from django.contrib.auth.models import User, Group
from django.db import transaction
from rest_framework.generics import get_object_or_404
from wallets.models import Wallet, Currency
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from wallets.serializers import *
from wallets.permissions import IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class WalletListView(generics.ListCreateAPIView):
    permission_classes = [IsOwner, IsAdminUser]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletRenameView(generics.RetrieveUpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletRenameSerializer


class WalletDepositView(APIView):
    def put(self, request, pk):
        data = request.data
        wallet = get_object_or_404(Wallet, id=pk)
        amount = data['amount']
        serializer = WalletDepositSerializer(wallet, data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    wallet.amount += amount
                    wallet.save()
            except Exception as e:
                return Response({"error": f"Transaction failed: {str(e)}"}, status=500)
            return Response({"message": "Transaction success"})


class WalletTransferView(APIView):
    #1. прописать логику конверсии
    #2. прописать остальные логики эндпоинтов
    #3. написать и применить serializer (validated data)
    #4. написать celery
    def put(self, request, pk):
        data = request.data
        wallet_from = get_object_or_404(Wallet, id=pk)
        serializer = WalletTransferSerializer(Wallet, data=data, context={"wallet_from_amount" : wallet_from.amount})
        serializer.is_valid(raise_exception=True)

        wallet_to = Wallet.objects.get(pk=data['wallet_to_id'])
        amount = data['amount']
        ratio = 1
        currency_from = Currency.objects.get(pk=wallet_from.currency.id)
        currency_to = Currency.objects.get(pk=wallet_to.currency.id)
        if currency_from.code != currency_to.code:
            ratio = currency_from.ratio / currency_to.ratio
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

    def put(self, request, pk):
        data = request.data
        wallet = get_object_or_404(Wallet, id=pk)
        amount = data['amount']
        serializer = WalletWithdrawSerializer(Wallet, data=data)
        if serializer.is_valid(raise_exception=True):
            try:
                with transaction.atomic():
                    wallet.amount -= amount
                    wallet.save()
            except Exception as e:
                return Response({"error": f"Transaction failed: {str(e)}"}, status=500)
            return Response({"message": "Transaction success"})


class WalletDeleteView(generics.DestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class CurrenciesView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrenciesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    