from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('accounts.urls')), # URLs de contas
    path('products/', include('products.urls')), # URLs de Produtod
    path('cart/', include('cart.urls')), # inclui as URLS do 
    path('orders/', include('orders.urls')) # inclui as URLs de ordem
]
