#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for tracking models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_scraped import models
from calaccess_scraped.admin.base import BaseAdmin


@admin.register(models.ScrapedDataVersion)
class ScrapedDataVersionAdmin(BaseAdmin):
    """
    Custom admin for the ScrapedDataVersion model.
    """
    list_display = (
        "id",
        "process_start_datetime",
        "process_finish_datetime"
    )
    list_display_links = ('process_start_datetime',)
    list_filter = ("process_finish_datetime",)
