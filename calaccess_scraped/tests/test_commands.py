#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
# from django.core.management import call_command
from django.test import TestCase
from calaccess_scraped.management.commands import CalAccessCommand


class ScrapedDataCommandsTest(TestCase):
    """
    Run and test management commands.
    """
    fixtures = [
        'calaccess_scraped/fixtures/candidate_scraped_elections.json',
        'calaccess_scraped/fixtures/scraped_candidates.json',
        'calaccess_scraped/fixtures/incumbent_scraped_elections.json',
        'calaccess_scraped/fixtures/scraped_incumbents.json',
        'calaccess_scraped/fixtures/proposition_scraped_elections.json',
        'calaccess_scraped/fixtures/scraped_propositions.json',
    ]

    def test_commands(self):
        """
        Run the scraping commands.
        """
        pass

    def test_base_command(self):
        """
        Test options on base commands.
        """
        c = CalAccessCommand()
        c.handle()
        c.header("")
        c.log("")
        c.success("")
        c.warn("")
        c.failure("")
        c.duration()
