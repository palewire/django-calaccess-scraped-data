#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for scraped candidate models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_scraped import models
from calaccess_scraped.admin.base import BaseAdmin


@admin.register(models.IncumbentElection)
class IncumbentElectionAdmin(BaseAdmin):
    """
    Custom admin for IncumbentElectionAdmin model.
    """
    list_display = (
        "name",
        "date"
    )
    list_per_page = 500
    search_fields = ("name",)


@admin.register(models.Incumbent)
class IncumbentAdmin(BaseAdmin):
    """
    Custom admin for IncumbentAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "category",
        "office_name",
        "session"
    )
    list_filter = (
        "category",
        "office_name",
        "session"
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "category",
        "office_name"
    )
