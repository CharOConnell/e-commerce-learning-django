from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        # files for the image if it's submitted
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        # render an empty product in our form

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    # get the product details
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        # put the info in
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
