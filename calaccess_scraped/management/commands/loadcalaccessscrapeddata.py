#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all scraper commands.
"""
# Files
import os
import csv
from calaccess_scraped import get_data_directory

# Time
from django.utils.timezone import now

# Django
from calaccess_scraped import models
from calaccess_scraped.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Run all scraper commands.
    """
    help = "Scrape CAL-ACCESS data and sync it with the database"
    data_dir = get_data_directory()

    def add_arguments(self, parser):
        """
        Adds custom arguments specific to this command.
        """
        parser.add_argument(
            '--flush',
            action='store_true',
            dest='force_flush',
            default=False,
            help='Flush database tables'
        )

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        # Parse the arguments
        self.force_flush = options.get("force_flush")

        # Flush, if asked for.
        if self.force_flush:
            self.flush()

        # Sync the scrape with the database.
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

    def open_csv(self, model):
        """
        Returns a DictReader with all the scraped records for the provided model.
        """
        file_name = "{}Item.csv".format(model().klass_name)
        file_path = os.path.join(self.data_dir, file_name)
        with open(file_path, 'r') as file_obj:
            file_reader = list(csv.DictReader(file_obj))
            if self.verbosity:
                self.log("Syncing {} {} scraped items".format(len(file_reader), model().klass_name))
            return file_reader

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
            self.save_row(models.PropositionElection, name=d['name'], url=d['url'])

        for d in self.open_csv(models.Proposition):
            self.save_row(
                models.Proposition,
                name=d['name'],
                scraped_id=d['id'],
                url=d['url'],
                election=models.PropositionElection.objects.get(name=d['election_name'])
            )

        for d in self.open_csv(models.PropositionCommittee):
            self.save_row(
                models.PropositionCommittee,
                name=d['name'],
                scraped_id=d['id'],
                position=d['position'],
                url=d['url'],
                proposition=models.Proposition.objects.get(name=d['proposition_name'])
            )

        for d in self.open_csv(models.IncumbentElection):
            self.save_row(
                models.IncumbentElection,
                session=d['session'],
                name=d['name'],
                date=d['date'],
                url=d['url'],
            )

        for d in self.open_csv(models.Incumbent):
            self.save_row(
                models.Incumbent,
                session=d['session'],
                category=d['category'],
                office_name=d['office'],
                name=d['name'],
                url=d['url'],
                scraped_id=d['id']
            )

        for d in self.open_csv(models.CandidateElection):
            self.save_row(
                models.CandidateElection,
                name=d['name'],
                scraped_id=d['id'],
                url=d['url'],
            )

        for d in self.open_csv(models.Candidate):
            self.save_row(
                models.Candidate,
                name=d['name'],
                scraped_id=d['id'],
                office_name=d['office'],
                url=d['url'],
                election=models.CandidateElection.objects.get(scraped_id=d['election_id']),
            )
