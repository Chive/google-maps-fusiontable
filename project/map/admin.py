# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'address',
        'latitude',
        'longitude',
        'created_at',
    )

    readonly_fields = (
        'address',
        'latitude',
        'longitude',
        'created_at',
    )
