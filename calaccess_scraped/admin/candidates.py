#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Custom administration panels for scraped candidate models.
"""
from __future__ import unicode_literals
from django.contrib import admin
from calaccess_scraped import models
from calaccess_scraped.admin.base import BaseAdmin


@admin.register(models.CandidateElection)
class CandidateElectionAdmin(BaseAdmin):
    """
    Custom admin for CandidateElectionAdmin model.
    """
    list_display = ("name",)
    list_per_page = 500
    search_fields = ("name",)


@admin.register(models.Candidate)
class CandidateAdmin(BaseAdmin):
    """
    Custom admin for CandidateAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "office_name",
        "election"
    )
    list_filter = (
        "election__name",
        "office_name"
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "office_name"
    )


@admin.register(models.CandidateCommittee)
class CandidateCommitteeAdmin(BaseAdmin):
    """
    Custom admin for CandidateCommitteeAdmin model.
    """
    list_display = (
        "scraped_id",
        "name",
        "candidate_id",
        "status"
    )
    list_per_page = 500
    search_fields = (
        "scraped_id",
        "name",
        "candidate_id",
        "status"
    )
