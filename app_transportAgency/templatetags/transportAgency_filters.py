from django import template
from app_transportAgency.models import Route, Ticket
from django.db.models import Count

register = template.Library()

@register.filter
def price_route(route):
    return Route.objects.filter(pk=route).first().precio

@register.simple_tag
def client_seating(date, route):
    return Ticket.objects.filter(ticket_reservation=date, routes=route).annotate(seats=Count('client'))
