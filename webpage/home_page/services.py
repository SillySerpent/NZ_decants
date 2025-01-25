from webpage.domain_model.domain_model import Cologne, Cart, User

featured_colognes = list[type[Cologne]]

def add_cologne_to_cart(cologne: Cologne, cart: Cart):
    return None


def add_cologne_to_featured_colognes(cologne: Cologne):

    if cologne in featured_colognes:
        raise ValueError('Cologne already added to featured colognes')
    elif len(featured_colognes) > 6:
        raise ValueError('Max number of featured cologne is 6')

    featured_colognes.append(cologne)


def remove_cologne_from_cart(cologne: Cologne):
    if cologne in featured_colognes:
        featured_colognes.remove(cologne)
    elif cologne not in featured_colognes:
        raise ValueError('Cologne not in featured colognes')