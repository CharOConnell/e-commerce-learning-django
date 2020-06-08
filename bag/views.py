from django.shortcuts import render, redirect


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    quantity = int(request.POST.get('quantity'))
    # it will come out of the form as a string so change it
    redirect_url = request.POST.get('redirect_url')
    # so we can send it back to the same page
    # we want to add to the browser session,
    # so it will only go after shutting browser
    bag = request.session.get('bag', {})
    # see if it's there, if not, create an empty dictionary

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        # if it already exists, add to it
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    # overwrite the data if it's there
    return redirect(redirect_url)
