from django import template

register = template.Library()

@register.filter(is_safe=True)
def amount_cal(amount):
    x=amount*0.75
    return round(x,2)


@register.filter(is_safe=True)
def interest_per_day(interest):
    return round(interest/30,2)

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