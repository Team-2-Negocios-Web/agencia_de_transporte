from django import template
from app_transportAgency.models import Route

register = template.Library()

@register.filter
def price_route(route):
    return Route.objects.filter(pk=route).first().precio