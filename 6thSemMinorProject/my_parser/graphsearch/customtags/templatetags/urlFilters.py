from django import template
from django.conf import settings

register = template.Library()

@register.filter('absoluteUrl')
def makeAbsoluteUrl(value):
	return settings.BASE_URL + value
