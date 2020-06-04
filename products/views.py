from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
# to generate a search query
from .models import Product


def all_products(request):
    """ A view to show all products, including
    sorting and searching queries """

    products = Product.objects.all()
    query = None
    # just set it to None so if there's nothing there it won't crap out

    if request.GET:
        # if it exists, we need to show only the filtered products
        if 'q' in request.GET:
            # what we named the search name
            query = request.GET['q']
            if not query:
                # if it is blank
                messages.error(request, "You didn't \
                    enter any search criteria!")
                return redirect(reverse('products'))
                # redirect back to the normal products url

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            # set a Q object where name contains query OR description
            # we also have the "i" which makes it case insensitive
            products = products.filter(queries)
            # passed to the filter method to filter products

    context = {
        'products': products,
        'search_term': query,
    }
    return render(request, 'products/products.html', context)
    # context as we'll need to send stuff back to the template


def product_detail(request, product_id):
    """ A view to show individual product details"""

    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)
    # context as we'll need to send stuff back to the template
