from django import template

register = template.Library()

@register.filter
@register.filter
def pluck(value, key):
    result = []
    for item in value:
        try:
            # Si es diccionario
            if isinstance(item, dict):
                result.append(item.get(key))
            # Si es objeto con atributo
            elif hasattr(item, key):
                result.append(getattr(item, key))
        except:
            continue
    #print(f"Pluck filter applied on {value} with key {key}, result: {result}")
    return result


@register.filter
def unique(value):
    return list(set(value))
