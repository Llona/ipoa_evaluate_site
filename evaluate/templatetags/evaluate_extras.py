from django import template

register = template.Library()

@register.filter
def replace_eol(value):
    return value.replace(r"\n", "<br>")

@register.filter
def append_str(str1, str2):
    return str("%s%s" % (str1, str2))
