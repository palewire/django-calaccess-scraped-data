#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from .base import BaseAdmin
from .candidates import (
    CandidateElectionAdmin,
    CandidateAdmin,
    CandidateCommitteeAdmin,
)
from .incumbents import (
    IncumbentElectionAdmin,
    IncumbentAdmin,
)
from .propositions import (
    PropositionElectionAdmin,
    PropositionAdmin,
    PropositionCommitteeAdmin,
)
from .tracking import (
    ScrapedDataVersionAdmin,
)

__all__ = (
    'BaseAdmin',
    'ScrapedDataVersionAdmin',
    'CandidateElectionAdmin',
    'CandidateAdmin',
    'CandidateCommitteeAdmin',
    'IncumbentElectionAdmin',
    'IncumbentAdmin',
    'PropositionElectionAdmin',
    'PropositionAdmin',
    'PropositionCommitteeAdmin',
)
