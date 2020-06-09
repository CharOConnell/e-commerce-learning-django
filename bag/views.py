from django.shortcuts import render, redirect, reverse, HttpResponse


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    quantity = int(request.POST.get('quantity'))
    # it will come out of the form as a string so change it
    redirect_url = request.POST.get('redirect_url')
    # so we can send it back to the same page

    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
        # if it exists, set it equal to it

    # we want to add to the browser session,
    # so it will only go after shutting browser
    bag = request.session.get('bag', {})
    # see if it's there, if not, create an empty dictionary

    if size:
        # see if the bag has the size in it
        if item_id in list(bag.keys()):
            # if item is already in the bag
            if size in bag[item_id]['items_by_size'].keys():
                # see if the same item in that size is there
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # this is a new size for that item
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            # if the item is not already in the bag, we need to add
            # it as a dictionary
            # key of items by size as it might need to buy different sizes
    else:
        # if no size we run this logic
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            # if it already exists, add to it
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    # overwrite the data if it's there
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the shopping bag """
    quantity = int(request.POST.get('quantity'))
    # it will come out of the form as a string so change it

    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
        # if it exists, set it equal to it

    # we want to add to the browser session,
    # so it will only go after shutting browser
    bag = request.session.get('bag', {})
    # see if it's there, if not, create an empty dictionary

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            # change that size item by the reduction/gain
        else:
            del bag[item_id]['items_by_size'][size]
            # quantity = 0 so delete
            if not bag[item_id]['items_by_size']:
                # if that makes that entire item dictionary empty,
                # let's delete that too
                bag.pop(item_id)
    else:
        # if no size we run this logic
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)
            # built in function to delete

    request.session['bag'] = bag
    # overwrite the data if it's there
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
            # if it exists, set it equal to it

        # we want to add to the browser session,
        # so it will only go after shutting browser
        bag = request.session.get('bag', {})
        # see if it's there, if not, create an empty dictionary

        if size:
            # if the size exists, we only want to delete that
            # size of that product
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                # if that makes that entire item dictionary empty,
                # let's delete that too
                bag.pop(item_id)
        else:
            # if no size we run this logic
            bag.pop(item_id)
            # built in function to delete

        request.session['bag'] = bag
        # overwrite the data if it's there
        return HttpResponse(status=200)
        # item was successfully removed
    except Exception as e:
        return HttpResponse(status=500)
