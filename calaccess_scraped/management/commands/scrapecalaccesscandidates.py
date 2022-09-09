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


# Django
from calaccess_scraped.management.commands import CalAccessCommand


class Command(CalAccessCommand):
    """
    Scrape the candidate data.
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
        candidate_list = []
        for html_path in html_list:
            print(html_path)
            with open(html_path, 'r') as f:
                html = f.read()
            soup = BeautifulSoup(html, 'html.parser')

            election_id = int(os.path.basename(html_path).replace(".html", ""))
            url = f"https://cal-access.sos.ca.gov/Campaign/Candidates/list.aspx?view=certified&electNav={election_id}"

            links = soup.find_all('a', href=re.compile(r'^.*&electNav=\d+'))
            this_link = [link for link in links if 'electNav={}'.format(election_id) in link['href']][-1]

            name = this_link.find_next_sibling('span').text.strip()

            election_dict = dict(
                url=url,
                id=election_id,
                name=name,
                year=int(name[:4])
            )
            election_list.append(election_dict)

            # Parse out the candidates
            for section in soup.findAll('a', {'name': re.compile(r'[a-z]+')}):

                # Check that this data matches the structure we expect.
                section_name_el = section.find('span', {'class': 'hdr14'})

                # If it doesn't, skip this one
                if not section_name_el:
                    continue

                # Loop through all the rows in the section table
                for office in section.findAll('td'):

                    # Check that this data matches the structure we expect.
                    title_el = office.find('span', {'class': 'hdr13'})

                    # If it doesn't, skip
                    if not title_el:
                        continue

                    # Pull the candidates out
                    for c in office.findAll('a', {'class': 'sublink2'}):
                        candidate_dict = dict(
                            office=title_el.text.strip(),
                            election_id=election_id,
                            id=re.match(r'.+id=(\d+)', c['href']).group(1),
                            name=c.text.strip(),
                            url=url
                        )
                        candidate_list.append(candidate_dict)

                    for c in office.findAll('span', {'class': 'txt7'}):
                        candidate_dict = dict(
                            office=title_el.text.strip(),
                            election_id=election_id,
                            id="",
                            name=c.text.strip(),
                            url=url
                        )
                        candidate_list.append(candidate_dict)

        with open(os.path.join(self.data_dir, 'CandidateElectionItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["url", "id", "name", "year"])
            writer.writeheader()
            writer.writerows(sorted(election_list, key=lambda x: x['year'], reverse=True))

        with open(os.path.join(self.data_dir, 'CandidateItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["url", "election_id", "id", "office", "name"])
            writer.writeheader()
            writer.writerows(candidate_list)
