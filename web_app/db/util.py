from web_app.db.models import Building


def find_by_address(street, number):
    return Building.nodes.first(street__exact=street, housenumber__exact=number)
