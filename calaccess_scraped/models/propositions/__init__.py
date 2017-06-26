#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing proposition information scraped from the CAL-ACCESS website.
"""
from .propositions import ScrapedProposition
from .elections import PropositionScrapedElection
from .committees import ScrapedPropositionCommittee


__all__ = (
    'ScrapedProposition',
    'PropositionScrapedElection',
    'ScrapedPropositionCommittee',
)
