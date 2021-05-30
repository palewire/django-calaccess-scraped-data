#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unittests for management commands.
"""
# from django.core.management import call_command
from django.test import TestCase
from django.core.management import call_command
from calaccess_scraped.management.commands import CalAccessCommand


class ScrapedDataCommandsTest(TestCase):
    """
    Run and test management commands.
    """
    def test_commands(self):
        """
        Run the scraping commands.
        """
        call_command("loadcalaccessscrapeddata")

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
