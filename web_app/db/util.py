from neomodel import Q

from web_app.db.models import Building


def find_by_address(street, number):
    # return Building.nodes.first(street__icontains=street, housenumber__icontains=number)
    return Building.nodes.filter(Q(street__icontains=street) | Q(street__contains=street), Q(housenumber__exact=number))[0]
