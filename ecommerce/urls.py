from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')), # Home Page
    #path('accounts/', include('accounts.urls')), # URLs de contas
    path('products/', include('products.urls')), # URLs de Produtod
    path('cart/', include('cart.urls')), # inclui as URLS do 
    path('orders/', include('orders.urls')), # inclui as URLs de ordem
    path('checkout/', include('checkout.urls')),
]
# Adicionando configuração para servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)