#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all scraper commands.
"""
import os
import json
import collections
from calaccess_scraped import models
from django.utils.timezone import now
from scrapy.crawler import CrawlerProcess
from django.core.management import call_command
from scrapy.utils.project import get_project_settings
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
        super(ScrapeCommand, self).handle(*args, **options)
        #self.scrape()
        self.load()

    def flush(self):
        """
        Delete records form related database tables.
        """
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
        process.crawl('incumbents')
        process.crawl('propositions')
        process.crawl('candidates')
        process.start()

    def load(self):
        scraped_path = os.path.join(self.cache_dir, 'scraped.json')
        grouped_dict = collections.defaultdict(list)
        with open(scraped_path, 'r') as f:
            for row in f.readlines():
                try:
                    d = json.loads(row)
                    grouped_dict[d['type']].append(d)
                except ValueError:
                    print(row)

        #
        # Propositions
        #

        for d in grouped_dict['PropositionElection']:
            election_obj, c = models.PropositionElection.objects.get_or_create(
                name=d['name'],
                url=d['url'],
            )
            if c and self.verbosity > 2:
                self.log('Created %s' % election_obj)
            if not c:
                election_obj.last_modified = now()
                election_obj.save()
        #
        # # Loop through propositions
        # for prop_data in prop_list:
        #     # Get or create proposition object
        #     prop_obj, c = Proposition.objects.get_or_create(
        #         name=prop_data['name'].strip(),
        #         scraped_id=prop_data['id'],
        #         url=prop_data['url'],
        #         election=election_obj
        #     )
        #     # Log it
        #     if c and self.verbosity > 2:
        #         self.log('Created %s' % prop_obj)
        #     else:
        #         prop_obj.last_modified = now()
        #         prop_obj.save()
        #
        # # Now loop through the committees
        # for committee in committee_list:
        #     # Get or create it
        #     committee_obj, c = PropositionCommittee.objects.get_or_create(
        #             name=committee['name'],
        #             scraped_id=committee['id'],
        #             position=committee['position'],
        #             url=committee['url'],
        #             proposition=prop_obj,
        #         )
        #
        #     # Log it
        #     if c and self.verbosity > 2:
        #         self.log('Created %s' % committee_obj)
        #     else:
        #         committee_obj.last_modified = now()
        #         committee_obj.save()
