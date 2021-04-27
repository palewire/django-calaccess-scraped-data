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
from datetime import datetime
from bs4 import BeautifulSoup
from calaccess_scraped import get_data_directory, get_html_directory

# Time
from django.utils.timezone import now

# Django
from calaccess_scraped.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Scrape the candidate data
    """
    help = "Scrape CAL-ACCESS data and sync it with the database"
    data_dir = get_data_directory()
    html_dir = get_html_directory()
    election_pattern = re.compile(r'^\d+\. (.+)\s+(?:[A-Z][a-z]+day), (\d{1,2}\/\d{1,2}\/\d{2})$')

    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(Command, self).handle(*args, **options)

        html_list = glob.glob(os.path.join(self.html_dir, "incumbents/*.html"))
        election_list = []
        candidate_list = []
        for html_path in html_list:
            with open(html_path, 'r') as f:
                html = f.read()
            soup = BeautifulSoup(html, 'html.parser')
        
            election_id = int(os.path.basename(html_path).replace(".html", ""))
            url = f"http://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=incumbent&session={election_id}"
        
            span_list = soup.find_all('span', class_='txt7')
            for span in span_list:
                match = self.election_pattern.match(span.text)
                if match:
                    election_dict = {
                        'session': int(election_id),
                        'name': match.groups()[0].strip(),
                        'date': str(datetime.strptime(match.groups()[1], '%m/%d/%y').date()),
                        'url': url
                    }
                    election_list.append(election_dict)

            sections = soup.find_all(
                'table',
                {
                    'cellspacing': 0,
                    'cellpadding': 4,
                    'border': 3,
                    'bordercolor': "#3149AA",
                    'bgcolor': "#7183C6",
                    'width': "100%",
                }
            )
            for section in sections:
                category = section.find('span', class_='hdr14').text.strip()
                for td in section.find_all('td', width="50%"):
                    office = td.find('span', class_='txt7').text.strip()
                    for a in td.find_all('a', class_='sublink2'):
                        incumbent_dict = {
                            'id': re.search(r'&id=(\d+)', a['href'].strip()).groups()[0],
                            'session': int(election_id),
                            'category': category,
                            'office': office,
                            "name": a.text.strip(),
                            "url": a['href'].strip()
                        }
                        candidate_list.append(incumbent_dict)

        with open(os.path.join(self.data_dir, 'IncumbentElectionItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["session", "name", "date", "url"])
            writer.writeheader()
            writer.writerows(sorted(election_list, key=lambda x: x['session'], reverse=True))

        with open(os.path.join(self.data_dir, 'IncumbentItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["id", "session", "category", "office", "name", "url"])
            writer.writeheader()
            writer.writerows(sorted(candidate_list, key=lambda x: x['session'], reverse=True))
