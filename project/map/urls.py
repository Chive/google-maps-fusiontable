from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.MapView.as_view(),
        name='map',
    ),
    url(
        r'^lookup/$',
        views.LookupCoordinatesView.as_view(),
        name='lookup-coordinates',
    ),
    url(
        r'^locations/$',
        views.GetMapLocationsView.as_view(),
        name='get-locations',
    ),
    url(
        r'^locations/clear/$',
        views.ClearMapLocationsView.as_view(),
        name='clear-locations',
    ),
]
