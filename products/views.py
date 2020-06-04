from django.shortcuts import render
from .models import Product


def all_products(request):
    """ A view to show all products, including
    sorting and searching queries """

    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/products.html', context)
    # context as we'll need to send stuff back to the template
