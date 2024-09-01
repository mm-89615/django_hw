from django.shortcuts import render, redirect
from .models import Phone

ORDERING = {
    'name': 'name',
    'min_price': 'price',
    'max_price': '-price',
}

def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    ordering = request.GET.get('sort', 'name')
    phones = Phone.objects.all().order_by(ORDERING[ordering])
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {"phone": phone}
    return render(request, template, context)
