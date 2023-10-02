from django import template
from time import time

register = template.Library()


@register.simple_tag
def timestamp():
    return int(time())


def render_datetime(dt):
    return dt.strftime("%Y-%m-%d %H:%M")


register.filter("render_datetime", render_datetime)
