#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing committee information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from django.db import models
from calaccess_scraped.models.base import BaseScrapedCommittee


class CandidateCommittee(BaseScrapedCommittee):
    """
    A candidate committee scraped from the California Secretary of State's site.
    """
    candidate_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.name
