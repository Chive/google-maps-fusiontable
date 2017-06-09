from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView, View

import geocoder
from requests import RequestException
from googleapiclient.errors import HttpError

from . import fusiontable
from .models import Location


class MapView(TemplateView):
    """
    Shows the map and location list
    """
    template_name = 'map/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update(
            google_api_key=settings.GOOGLE_API_KEY,
            ft_doc_id=settings.GOOGLE_FUSIONTABLE_TABLE_ID,
            locations=Location.objects.all(),
        )
        return context


class LookupCoordinatesView(View):
    """
    Reverse-lookup coordinates with Google and store it 
    in our own Database and potentially FusionTable 
    if settings.SEND_LOCATIONS_TO_FUSIONTABLE is active
    """

    def post(self, request, *args, **kwargs):
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if not all((latitude, longitude)):
            return HttpResponseBadRequest()

        # let's try to reverse geocode the coordinates
        response = dict()

        try:
            lookup = geocoder.google(
                (latitude, longitude),
                method='reverse',
            )
        except RequestException:
            response.update(
                success=False,
                status='UNABLE_TO_GEOCODE',
            )
        else:

            if lookup.ok:
                address = lookup.address
                location, created = Location.create(
                    latitude=latitude,
                    longitude=longitude,
                    address=address,
                )

                response.update(
                    success=True,
                    address=address,
                )

                if not created:
                    response.update(status='DUPLICATE_LOCATION')
                elif settings.SEND_LOCATIONS_TO_FUSIONTABLE:
                    try:
                        # the FT takes a long time (1-2s)
                        # which slows the entire app down
                        fusiontable.insert_location(
                            location,
                            settings.GOOGLE_FUSIONTABLE_TABLE_ID,
                        )
                    except HttpError:
                        # Most likely: auth error or rate limit
                        response.update(
                            success=False,
                            status='UNABLE_TO_UPDATE_FUSIONTABLE',
                        )

            else:
                # geocoding has failed, this either
                # happens if location has no adddress
                # available (e.g in the sea or in a desert)
                # or if there was another error on Google's side
                response.update(
                    success=False,
                    status='UNABLE_TO_GEOCODE',
                )

        return JsonResponse(response)


class GetMapLocationsView(View):
    """
    Shows the list of saved locations,
    to be used on the Map view.
    """
    def get(self, request, *args, **kwargs):
        data = {
            'locations': [
                location.serialize()
                for location
                in Location.objects.all()
            ]
        }
        return JsonResponse(data)


class ClearMapLocationsView(View):
    """
    Clears the currently saved locations.
    
    Lacks authentication and authorization.
    """
    def post(self, request, *args, **kwargs):
        Location.objects.all().delete()
        if settings.SEND_LOCATIONS_TO_FUSIONTABLE:
            fusiontable.clear_table(settings.GOOGLE_FUSIONTABLE_TABLE_ID)
        return JsonResponse(dict(success=True))
