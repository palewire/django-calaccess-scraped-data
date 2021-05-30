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
import time
from bs4 import BeautifulSoup
from selenium import webdriver
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

        html_list = glob.glob(os.path.join(self.html_dir, "propositions/*.html"))
        election_list = []
        prop_list = []
        for html_path in html_list:
            with open(html_path, 'r') as f:
                html = f.read()

            soup = BeautifulSoup(html, "html.parser")

            election_id = int(os.path.basename(html_path).replace(".html", ""))
            url = f"https://cal-access.sos.ca.gov/Campaign/Measures/list.aspx?session={election_id}"
            table_list = soup.find_all("table", id=re.compile("^ListElections1__"))
            # Parse out all the elections
            for table in table_list:
                election_dict = {
                    'name': table.caption.span.text,
                    'url': url,
                    'year': election_id,
                }
                election_list.append(election_dict)
                prop_urls = table.find_all("a")
                for a in prop_urls:
                    prop_dict = dict(
                        url="http://cal-access.sos.ca.gov/Campaign/Measures/" + a['href'],
                        election_name=election_dict['name'],
                        id=re.match(r'.+id=(\d+)', a['href']).group(1),
                        name=a.text
                    )
                    prop_list.append(prop_dict)

        with open(os.path.join(self.data_dir, 'PropositionElectionItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "url", "year"])
            writer.writeheader()
            writer.writerows(sorted(election_list, key=lambda x: x['year'], reverse=True))

        with open(os.path.join(self.data_dir, 'PropositionItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["url", "election_name", "id", "name"])
            writer.writeheader()
            writer.writerows(prop_list)

        committee_list = []
        for prop in prop_list:
            html_path = os.path.join(self.html_dir, 'proposition_committees', prop['id'] + ".html")
            if os.path.exists(html_path):
                print(f"Opening {html_path}")
            else:
                print(f"Downloading {prop['url']}")
                fireFoxOptions = webdriver.FirefoxOptions()
                fireFoxOptions.set_headless()
                browser = webdriver.Firefox(firefox_options=fireFoxOptions)
                browser.get(prop['url'])
                with open(html_path, 'w') as f:
                    f.write(browser.page_source)
                browser.close()
                time.sleep(1)

            with open(html_path, 'r') as f:
                html = f.read()

            prop_soup = BeautifulSoup(html, "html.parser")
            for table in prop_soup.findAll('table', cellpadding='4'):
                for row in table.find_all("tr")[1:]:
                    cell_list = row.find_all("td")
                    committee_dict = dict(
                        election_name=prop['election_name'],
                        proposition_id=prop['id'],
                        proposition_name=prop['name'],
                        id=cell_list[0].text,
                        name=cell_list[1].text,
                        position=cell_list[2].text,
                        url="http://cal-access.sos.ca.gov" + cell_list[1].a['href']
                    )
                    committee_list.append(committee_dict)

        with open(os.path.join(self.data_dir, 'PropositionCommitteeItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "election_name",
                "proposition_id",
                "proposition_name",
                "id",
                "name",
                "position",
                "url"
            ])
            writer.writeheader()
            writer.writerows(committee_list)
