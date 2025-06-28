from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def add_query_param(context: dict, **kwargs) -> str:
    request = context["request"]
    request_params = request.GET.copy()
    for key, value in kwargs.items():
        request_params[key] = value

    return f"?{request_params.urlencode()}"
