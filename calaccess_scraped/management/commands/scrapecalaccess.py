#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all scraper commands.
"""
import os
import json
import collections
from django.conf import settings
from calaccess_scraped import models
from django.utils.timezone import now
from scrapy.crawler import CrawlerProcess
from django.core.management import call_command
from scrapy.utils.project import get_project_settings
from calaccess_scraped.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Run all scraper commands.
    """
    help = "Run all scraper commands"
    cache_dir = os.path.join(
        settings.BASE_DIR,
        ".scraper_cache"
    )

    def add_arguments(self, parser):
        """
        Adds custom arguments specific to this command.
        """
        parser.add_argument(
            '--flush',
            action='store_true',
            dest='force_flush',
            default=False,
            help='Flush database tables',
        )
        parser.add_argument(
            '--cache-only',
            action='store_false',
            dest='update_cache',
            default=True,
            help="Skip the scraper's update checks. Use only cached files.",
        )

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        self.force_flush = options.get("force_flush")
        self.update_cache = options.get("update_cache")

        os.path.exists(self.cache_dir) or os.mkdir(self.cache_dir)

        if self.force_flush:
            self.flush()

        if self.update_cache:
            self.scrape()

        self.load()

    def get_scraped_version(self):
        """
        Get or create the current processed version.

        Return a tuple (ProcessedDataVersion object, created), where
        created is a boolean specifying whether a version was created.
        """
        return ScrapedDataVersion.objects.create()

    def flush(self):
        """
        Delete records form related database tables.
        """
        self.log("Flushing database")
        models.PropositionCommittee.objects.all().delete()
        models.Proposition.objects.all().delete()
        models.PropositionElection.objects.all().delete()
        models.Candidate.objects.all().delete()
        models.CandidateElection.objects.all().delete()
        models.Incumbent.objects.all().delete()
        models.IncumbentElection.objects.all().delete()

    def scrape(self):
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'calaccess_crawler.settings'
        os.environ['SCRAPY_ITEMS_PATH'] = os.path.join(self.cache_dir, 'scraped.json')
        process = CrawlerProcess(get_project_settings())
        #process.crawl('incumbents')
        process.crawl('propositions')
        #process.crawl('candidates')
        process.start()

    def save(self, model, **kwargs):
        obj, created = model.objects.get_or_create(**kwargs)
        if created and self.verbosity > 2:
            self.log('Created {}'.format(obj))
        if not created:
            obj.last_modified = now()
            obj.save()

    def load(self):
        # Read in the scraped data from JSON and regroup it by model.
        scraped_path = os.path.join(self.cache_dir, 'scraped.json')
        grouped_dict = collections.defaultdict(list)
        with open(scraped_path, 'r') as f:
            for row in f.readlines():
                try:
                    d = json.loads(row)
                    grouped_dict[d['type']].append(d)
                except ValueError:
                    print(row)

        # Load the models one by one.
        for d in grouped_dict['PropositionElection']:
            self.save(models.PropositionElection, name=d['name'], url=d['url'])

        for d in grouped_dict['Proposition']:
            self.save(
                models.Proposition,
                name=d['name'],
                scraped_id=d['id'],
                url=d['url'],
                election=models.PropositionElection.objects.get(name=d['election_name'])
            )

        for d in grouped_dict['PropositionCommittee']:
            self.save(
                models.PropositionCommittee,
                name=d['name'],
                scraped_id=d['id'],
                position=d['position'],
                url=d['url'],
                proposition=models.Proposition.objects.get(name=d['proposition_name'])
            )
