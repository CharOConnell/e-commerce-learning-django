from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.db.models import Q
# to generate a search query
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including
    sorting and searching queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    # just set it to None so if there's nothing there it won't crap out

    if request.GET:
        if 'sort' in request.GET:
            if 'direction' in request.GET:
                sortkey = request.GET['sort']
                sort = sortkey
                if sortkey == 'name':
                    sortkey = 'lower_name'
                    products = products.annotate(lower_name=Lower('name'))
                if sortkey == 'category':
                    sortkey = 'caetgory__name'
                    # allows us to drill into the related model
                if 'direction' in request.GET:
                    direction = request.GET['direction']
                    if direction == 'desc':
                        sortkey = f'-{sortkey}'
                products = products.order_by(sortkey)

        # if it exists, we need to show only the filtered products
        if 'category' in request.GET:
            # if it exists in search
            categories = request.GET['category'].split(',')
            # split up the data by the commas
            products = products.filter(category__name__in=categories)
            # filter all products whose category is in the list
            # we're looking for the name field in the category field
            categories = Category.objects.filter(name__in=categories)
            # we can display which category they have selected

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

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
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


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    # render an empty product in our form
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
