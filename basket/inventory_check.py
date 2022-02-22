""" Check basket against product inventory. """
from basket.contexts import basket_contents


def check_inventory(request):
    """
    Compare the basket items with the inventory field
    for each product and remove from basket if there are
    not enough available.
    """
    initial_basket = basket_contents(request)
    basket = request.session.get('basket')
    problem_items = []
    for item in initial_basket['basket_items']:
        if item['quantity'] > item['product'].inventory:
            basket.pop(item['item_id'])
            problem_items.append(item['product'].name)

    request.session['basket'] = basket

    return problem_items
