#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for storing proposition information scraped from the CAL-ACCESS website.
"""
from .propositions import Proposition
from .elections import PropositionElection
from .committees import PropositionCommittee


__all__ = (
    'Proposition',
    'PropositionElection',
    'PropositionCommittee',
)
