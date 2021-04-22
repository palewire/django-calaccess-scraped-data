#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing candidate information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_scraped.models.base import BaseScrapedModel


class Candidate(BaseScrapedModel):
    """
    A candidate for office scraped from the California Secretary of State's site.
    """
    name = models.CharField(
        verbose_name="candidate name",
        max_length=200
    )
    scraped_id = models.CharField(
        verbose_name="candidate identification number",
        max_length=7,
        blank=True,  # Some don't have IDs on the website
    )
    office_name = models.CharField(
        verbose_name="name of the office for which this candidate is running",
        max_length=100,
        blank=True
    )
    election = models.ForeignKey(
        'CandidateElection',
        related_name='candidates',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
