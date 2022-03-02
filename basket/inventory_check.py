""" Check basket against product inventory. """
from basket.contexts import basket_contents


def check_inventory(request):
    """
    Compare the basket items with the inventory field
    for each product and remove from basket if there are
    not enough available.
    """
    basket = request.session.get('basket', {})
    problem_items = []
    initial_basket = basket_contents(request)
    # Iterate through the basket comparing quantity against inventory
    for item in initial_basket['basket_items']:
        if item['quantity'] > item['product'].inventory:
            # Remove out of stock items from basket
            basket.pop(item['item_id'])
            # Add out of stock product name to problem items list
            problem_items.append(item['product'].name)

    request.session['basket'] = basket

    # Return problem items list to the view so that it can generate a message
    # informing the user of the updated basket
    return problem_items
