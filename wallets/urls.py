from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wallets import views


app_name = 'wallets'
urlpatterns = [
    path('', views.WalletListView.as_view(), name='wallet-list'),
    path('<int:pk>/', views.WalletDetailView.as_view(), name='wallet-detail'),
    path('<int:pk>/rename', views.WalletRenameView.as_view(), name='wallet-rename'),
    path('<int:pk>/deposit', views.WalletDepositView.as_view(), name='wallet-deposit'),
    path('<int:pk>/transfer', views.WalletTransferView.as_view(), name='wallet-transfer'),
    path('<int:pk>/withdraw', views.WalletWithdrawView.as_view(), name='wallet-withdraw'),
    path('<int:pk>/delete', views.WalletDeleteView.as_view(), name='wallet-delete'),
]