from django import template

register = template.Library()


@register.filter
def rub(value):
    if value is None:
        return '0,00 руб.'
    try:
        formatted = f'{float(value):.2f}'
        parts = formatted.split('.')
        int_part = parts[0]
        result = ''
        for i, ch in enumerate(reversed(int_part)):
            if i > 0 and i % 3 == 0:
                result = ' ' + result
            result = ch + result
        return f'{result},{parts[1]} руб.'
    except (ValueError, TypeError):
        return '0,00 руб.'
