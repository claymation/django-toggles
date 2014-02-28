django-toggles
==============

Easily add dynamic two-state toggle buttons to your Django project.

Building the user interface for a feature like these?

* friending
* following
* liking

The common thread among these features is that they have binary states:
you're either friends or you aren't; you either like something or you don't.

The UI for these kinds of features often includes a binary toggle switch,
implemented as an HTML5 `<button>` element that, when clicked, makes an XHR
request to change state on the server.

This reusable Django app includes views, template tags, and scripts to make
implementing these features quick and painless.


Usage
-----

* Install the library:

        pip install django-toggles

* Add "toggles" to `INSTALLED_APPS`

* Subclass ToggleView (or AuthenticatedToggleView):

        from toggles.views import ToggleView

        class MyToggleView(ToggleView):
            def put(self, request):
                """Set the toggle"""
                something.you.want.to.update = True

            def delete(self, request):
                """Clear the toggle"""
                something.you.want.to.update = False

* Wire up your ToggleView `URLconf`

        from django.conf.urls import patterns, include, url
    
        urlpatterns = patterns('',
            ...
            url(r'^rest/api/for/thing/to/toggle/$',
                MyToggle.as_view(),
                name="my_toggle"),
            ...
        )

* Render the toggle button in your templates:

        {% load toggles %}
        {% toggles_js %}
        ...
        {% url "my_toggle" as toggle_url %}
        {% toggle active=object.toggled url=toggle_url on="On" off="Off" %}

* That's it! Users visiting that page will see a button that reflects the current state of the toggle,
  and can click the button to dynamically change its state.


Examples
--------

### Liking objects

* Subclass AuthenticatedToggleView (to ensure request.user is present):

        from toggles.views import ToggleView

        class LikeToggleView(AuthenticatedToggleView):
            def put(self, request, object_pk):
                """
                Handle requests to like an object.
                """
                try:
                    request.user.liked_objects.add(object_pk)
                except IntegrityError:
                    return HttpResponseBadRequest()
                return HttpResponse()

            def delete(self, request, object_pk):
                """
                Handle requests to unlike an object.
                """
                try:
                    request.user.liked_objects.remove(object_pk)
                except IntegrityError:
                    return HttpResponseBadRequest()
                return HttpResponse()

* Wire up your LikeToggleView `URLconf`

        from django.conf.urls import patterns, include, url
    
        urlpatterns = patterns('',
            ...
            url(r'users/self/objects/liked/(?P<object_pk>[\d]+)/$',
                LikeToggleView.as_view(),
                name="user_objects_liked"),
            ...
        )

* Render the Like button in your templates:

        {% load toggles %}
        {% toggles_js %}
        ...
        {% url "user_objects_liked" object.pk as toggle_url %}
        {% toggle active=object.liked url=toggle_url on="You like this" off="Like" %}

* That's it! Users can now like content objects dynamically by clicking the Like button on the page.

Note: In this example, we have a M2M relationship between User and the objects that we're liking.
To avoid doing N+1 database queries in a list view (to determine if the user has already liked each object),
we set a `.liked` attribute on each object in one query with something like:

        liked_objects = []
        user = self.request.user
        if user.is_authenticated():
            liked_objects = frozenset(user.liked_objects.values_list('pk', flat=True))
        for obj in all_objects_to_be_displayed_on_this_page:
            obj.liked = obj.pk in liked_objects

If you're using class-based views, a good place to do this kind of thing is in `get_context_data`.
