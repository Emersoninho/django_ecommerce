from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.all().order_by('-created')[:4]
    return render(request, 'home/home.html', {'products': products})