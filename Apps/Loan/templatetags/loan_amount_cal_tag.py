from django import template
from datetime import *
register = template.Library()

@register.filter(is_safe=True)
def amount_cal(amount):
    x=amount*0.75
    return round(x,2)


@register.simple_tag
def todayAmount(x,y):
    try:
        return float(x)*float(y)
    except:
        return ""

@register.filter(is_safe=True)
def interestCal(intrest):
    x = intrest/30
    return round(x,2)

@register.filter(is_safe=True)
def No_of_day(loan_info_obj):
    aprove_date = loan_info_obj.added_date.date()
    today = date.today()
    if loan_info_obj.exit_date:
        today = loan_info_obj.exit_date.date()
    day = today - aprove_date
    day = day.days
    if day < 30:
        day = 30

    return day
