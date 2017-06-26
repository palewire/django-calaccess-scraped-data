#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from calaccess_raw.admin.base import BaseAdmin
from .candidates import (
    CandidateScrapedElectionAdmin,
    ScrapedCandidateAdmin,
    ScrapedCandidateCommitteeAdmin,
)
from .incumbents import (
    IncumbentScrapedElectionAdmin,
    ScrapedIncumbentAdmin,
)
from .propositions import (
    PropositionScrapedElectionAdmin,
    ScrapedPropositionAdmin,
    ScrapedPropositionCommitteeAdmin,
)
from .tracking import (
    ScrapedDataVersionAdmin,
)

__all__ = (
    'BaseAdmin',
    'ScrapedDataVersionAdmin',
    'CandidateScrapedElectionAdmin',
    'ScrapedCandidateAdmin',
    'ScrapedCandidateCommitteeAdmin',
    'IncumbentScrapedElectionAdmin',
    'ScrapedIncumbentAdmin',
    'PropositionScrapedElectionAdmin',
    'ScrapedPropositionAdmin',
    'ScrapedPropositionCommitteeAdmin',
)
