#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for scraped proposition models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_scraped import models
from calaccess_scraped.admin.base import BaseAdmin


@admin.register(models.PropositionElection)
class PropositionElectionAdmin(BaseAdmin):
    """
    Custom admin for PropositionElectionAdmin model.
    """
    list_display = ("name",)
    list_per_page = 500
    search_fields = ("name",)


@admin.register(models.Proposition)
class PropositionAdmin(BaseAdmin):
    """
    Custom admin for ScrapedPropositionAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "election"
    )
    list_filter = ("election",)
    list_per_page = 500
    search_fields = (
        "name",
        "scraped_id"
    )


@admin.register(models.PropositionCommittee)
class PropositionCommitteeAdmin(BaseAdmin):
    """
    Custom admin for PropositionCommitteeAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "position",
        "proposition"
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "position",
        "proposition"
    )
