#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all scraper commands.
"""
# Files
import os

# Scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Django
from django.conf import settings
from calaccess_scraped.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Run all scraper commands.
    """
    help = "Scrape CAL-ACCESS data and sync it with the database"
    cache_dir = os.path.join(settings.BASE_DIR, ".scraper_cache")

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)
        self.scrape()

    def scrape(self):
        """
        Use Scrapy to crawl the CAL-ACCESS website and harvest data.
        """
        # Configure Scrapy
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'calaccess_crawler.settings'
        os.environ['SCRAPY_EXPORT_DIR'] = self.cache_dir
        process = CrawlerProcess(get_project_settings())

        # Run the scrape
        process.crawl('incumbents')
        process.crawl('propositions')
        process.crawl('candidates')
        process.start()
        process.stop()
