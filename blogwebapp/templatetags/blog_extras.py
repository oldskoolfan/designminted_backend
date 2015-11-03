from django import template
from datetime import date

register = template.Library()

@register.simple_tag
def get_copyright():
    return "&copy; {0}".format(date.today().year)

@register.inclusion_tag('footer.html')
def include_footer():
    return
