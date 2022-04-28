from django.urls import include, path

from wallets import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('wallets/', include('wallets.urls')),
    path('currencies/', views.CurrenciesView.as_view(), name='currencies-list'),
    path('currencies/<int:pk>/', views.CurrenciesDetailView.as_view(), name='currency-detail'),
]