#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing candidate information scraped from the CAL-ACCESS website.
"""
from .candidates import ScrapedCandidate
from .elections import CandidateScrapedElection
from .committees import ScrapedCandidateCommittee

__all__ = (
    'ScrapedCandidate',
    'CandidateScrapedElection',
    'ScrapedCandidateCommittee',
)
