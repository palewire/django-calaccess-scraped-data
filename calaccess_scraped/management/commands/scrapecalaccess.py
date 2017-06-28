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
    help = "Run all scraper commands."

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        call_command(
            'scrapecalaccesspropositions',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_flush=self.force_flush,
            force_download=self.force_download,
            update_cache=self.update_cache,
        )

        call_command(
            'scrapecalaccesscandidates',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_flush=self.force_flush,
            force_download=self.force_download,
            update_cache=self.update_cache,
        )

        call_command(
            'scrapecalaccessincumbents',
            verbosity=self.verbosity,
            no_color=self.no_color,
            force_flush=self.force_flush,
            force_download=self.force_download,
            update_cache=self.update_cache,
        )
        # Should we be running scrapecalaccesscandidatecommittees too?
