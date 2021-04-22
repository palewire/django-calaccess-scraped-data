#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing election information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
from calaccess_scraped.models.base import BaseScrapedElection


class PropositionElection(BaseScrapedElection):
    """
    An election day scraped as part of the `scrapecalaccesspropositions` command.
    """
    def __str__(self):
        return self.name
