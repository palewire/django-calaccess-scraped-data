#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing proposition information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_scraped.models.base import BaseScrapedModel


class Proposition(BaseScrapedModel):
    """
    A yes or no ballot measure for voters scraped from the California Secretary of State's site.
    """
    # Most of the time, this is a number, however,
    # it can be a bona fide name, e.g.
    # '2003 Recall Question'
    name = models.CharField(
        verbose_name="proposition name",
        max_length=200
    )
    scraped_id = models.CharField(
        verbose_name="proposition identification number",
        max_length=200
    )
    election = models.ForeignKey(
        'PropositionElection',
        related_name='propositions',
        on_delete=models.CASCADE
    )

    class Meta:
        """
        Model options.
        """
        ordering = ("-election", "name")

    def __str__(self):
        return 'Proposition: {}'.format(self.name)
