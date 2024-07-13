# core/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def total_cost(selected_items):
    return sum(item.quantity * item.item.price for item in selected_items)



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


