from django import template
from app_transportAgency.models import Route, Ticket

register = template.Library()

@register.filter
def price_route(route):
    return Route.objects.filter(pk=route).first().precio

@register.simple_tag
def client_seating(date, route):
    return Ticket.objects.values('client','companion','seating').filter(ticket_reservation=date, routes=route)