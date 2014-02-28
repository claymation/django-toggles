from django.http import HttpResponseForbidden
from django.views.generic.base import View


class ToggleView(View):
    """
    Handles requests to turn on/off a toggle.
    """
    http_method_names = ('put', 'delete')


class AuthenticatedToggleView(ToggleView):
    """
    Extends ToggleView by requiring an authenticated user.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(AuthenticatedToggleView, self).dispatch(request, *args, **kwargs)
