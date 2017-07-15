#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all scraper commands.
"""
from django.core.management import call_command
from calaccess_scraped.management.commands import ScrapeCommand


class Command(ScrapeCommand):
    """
    Run all scraper commands.
    """
    help = "Run all scraper commands"

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        kwargs = dict(
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_flush=self.force_flush,
            force_download=self.force_download,
            update_cache=self.update_cache,
        )
        call_command('scrapecalaccesspropositions', **kwargs)
        call_command('scrapecalaccesscandidates', **kwargs)
        call_command('scrapecalaccessincumbents', **kwargs)
