from django import template

register = template.Library()

@register.inclusion_tag('ubu_dev_flag_img.html')
def ubu_dev_img(flag):
    return {'flag': flag}

@register.filter
def recent_contact(person):
    if person.contacts.all():
        return person.contacts.all().reverse()[0].submit_date
