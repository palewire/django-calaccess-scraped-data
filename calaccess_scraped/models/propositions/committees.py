#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing committee information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_scraped.models.base import BaseScrapedCommittee


class PropositionCommittee(BaseScrapedCommittee):
    """
    A committee supporting or opposing a proposition scraped from the California Secretary of State's site.
    """
    position = models.CharField(
        max_length=100,
        help_text="Whether the committee supports or opposes the proposition",
    )
    proposition = models.ForeignKey('Proposition', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
