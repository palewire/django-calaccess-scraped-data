#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all scraper commands.
"""
import os
import csv
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

        self.sync()

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
        """
        Use Scrapy to crawl the CAL-ACCESS website and harvest data.
        """
        os.environ['SCRAPY_SETTINGS_MODULE'] = 'calaccess_crawler.settings'
        os.environ['SCRAPY_EXPORT_DIR'] = self.cache_dir
        process = CrawlerProcess(get_project_settings())
        process.crawl('incumbents')
        process.crawl('propositions')
        process.crawl('candidates')
        process.start()

    def open_csv(self, model):
        """
        Returns a DictReader with all the scraped records for the provided model.
        """
        file_name = "{}Item.csv".format(model.klass_name)
        file_path = os.path.join(self.cache_dir, file_name)
        reader = list(csv.DictReader(open(file_path, 'r')))
        if self.verbosity:
            self.log("Syncing {} {} scraped items".format(len(reader), model.klass_name))

    def save_row(self, model, **row):
        """
        Syncs a CSV row of data to the provided model.
        """
        obj, created = model.objects.get_or_create(**row)
        if created and self.verbosity > 2:
            self.log('Created {}: {}'.format(obj.klass_name, obj))
        if not created:
            obj.last_modified = now()
            obj.save()

    def sync(self):
        """
        Syncs the scraped data with the database, model by model and row by row.
        """
        # Load the models one by one.
        for d in self.open_csv(models.PropositionElection):
            self.save(models.PropositionElection, name=d['name'], url=d['url'])

        for d in self.open_csv(models.Proposition):
            self.save(
                models.Proposition,
                name=d['name'],
                scraped_id=d['id'],
                url=d['url'],
                election=models.PropositionElection.objects.get(name=d['election_name'])
            )

        for d in self.open_csv(models.PropositionCommittee):
            self.save(
                models.PropositionCommittee,
                name=d['name'],
                scraped_id=d['id'],
                position=d['position'],
                url=d['url'],
                proposition=models.Proposition.objects.get(name=d['proposition_name'])
            )

        for d in self.open_csv(models.IncumbentElection):
            self.save(
                models.IncumbentElection,
                session=d['session'],
                name=d['name'],
                date=d['date'],
                url=d['url'],
            )

        for d in self.open_csv(models.Incumbent):
            self.save(
                models.Incumbent,
                session=d['session'],
                category=d['category'],
                office_name=d['office'],
                name=d['name'],
                url=d['url'],
                scraped_id=d['id']
            )
