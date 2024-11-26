from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('accounts.urls')), # URLs de contas
    #path('products/', include('products.urls')), # URLs de Produtod
]
