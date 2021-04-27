#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run all scraper commands.
"""
# Files
import re
import os
import csv
import glob
from bs4 import BeautifulSoup
from calaccess_scraped import get_data_directory, get_html_directory

# Time
from django.utils.timezone import now

# Django
from calaccess_scraped import models
from calaccess_scraped.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Scrape the candidate data
    """
    help = "Scrape CAL-ACCESS data and sync it with the database"
    data_dir = get_data_directory()
    html_dir = get_html_directory()

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        html_list = glob.glob(os.path.join(self.html_dir, "candidates/*.html"))
        election_list = []
        for html_path in html_list:
            with open(html_path, 'r') as f:
                html = f.read()
            soup = BeautifulSoup(html, 'html.parser')

            election_id = int(os.path.basename(html_path).replace(".html", ""))

            links = soup.find_all('a', href=re.compile(r'^.*&electNav=\d+'))
            this_link = [l for l in links if 'electNav={}'.format(election_id) in l['href']][-1]

            name = this_link.find_next_sibling('span').text.strip()
            
            election_dict = dict(
                url=f"https://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=certified&electNav={election_id}",
                id=election_id,
                name=name,
                year=int(name[:4])
            )
            election_list.append(election_dict)
        
        with open(os.path.join(self.data_dir, 'CandidateElectionItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["url", "id", "name", "year"])
            writer.writeheader()
            writer.writerows(sorted(election_list, key=lambda x: x['year'], reverse=True))
