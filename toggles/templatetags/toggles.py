from django import template

register = template.Library()


@register.inclusion_tag('toggles/toggles_js.html')
def toggles_js():
    return {}


@register.inclusion_tag('toggles/toggle.html')
def toggle(active, url, btnid=None, btncls="btn btn-primary", loading="Loading...", on="On", off="Off"):
    if active: btncls += " active"
    return {
        "active": "true" if active else "false",
        "url": url,
        "btnid": btnid,
        "btncls": btncls,
        "loading": loading,
        "on": on,
        "off": off,
        "label": on if active else off,
    }
