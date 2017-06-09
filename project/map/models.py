from django.db import models
from django.forms import model_to_dict
from django.utils.translation import ugettext_lazy as _


class Location(models.Model):
    created_at = models.DateTimeField(
        _('Date created'),
        auto_now_add=True,
    )

    latitude = models.DecimalField(
        _('Latitude'),
        max_digits=23,
        decimal_places=20,
    )

    longitude = models.DecimalField(
        _('Longitude'),
        max_digits=23,
        decimal_places=20,
    )

    address = models.TextField(
        _('Address'),
    )

    class Meta:
        ordering = (
            '-created_at',
        )

    def __str__(self):
        return 'Location <{}>'.format(self.address)

    @classmethod
    def create(cls, latitude, longitude, address):
        return cls.objects.get_or_create(
            address=address,
            defaults=dict(
                latitude=latitude,
                longitude=longitude,
            ),
        )

    def serialize(self):
        return model_to_dict(
            instance=self,
            fields=(
                'latitude',
                'longitude',
                'address',
            ),
        )
