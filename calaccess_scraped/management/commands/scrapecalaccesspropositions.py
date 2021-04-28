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
#                prop_urls = table.xpath("//a[@href]/@href")
#                for url in prop_urls:
#                    full_url = "http://cal-access.sos.ca.gov/Campaign/Measures" + url

        with open(os.path.join(self.data_dir, 'PropositionElectionItem.csv'), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=["name", "url", "year"])
            writer.writeheader()
            writer.writerows(sorted(election_list, key=lambda x: x['year'], reverse=True))

#                    full_url = urljoin("http://cal-access.sos.ca.gov/Campaign/Measures/", url)
#                    yield scrapy.Request(
#                        url=full_url,
#                        callback=self.parse_proposition,
#                        meta={
#                            "election_name": name,
#                        }
#                    )

#    def parse_proposition(self, response):
#        """
#        Scrape all the committees from proposition detail pages.
#        """
#        soup = BeautifulSoup(response.body, 'lxml')

#        proposition_name = soup.find('span', id='measureName').text
#        proposition_id = re.match(r'.+id=(\d+)', response.url).group(1)

#        prop = PropositionLoader()
#        prop.add_value("id", proposition_id)
#        prop.add_value("name", proposition_name)
#        prop.add_value("election_name", response.meta['election_name'])
#        prop.add_value("url", response.url)
#        yield prop.load_item()

#        # Loop through all the tables on the page
#        # which contain the committees on each side of the measure
#        for table in soup.findAll('table', cellpadding='4'):
#            item = PropositionCommitteeLoader(response=response)
#            item.add_value("election_name", response.meta['election_name'])
#            item.add_value("proposition_name", proposition_name)
#            item.add_value("proposition_id", proposition_id)

#            # Pull the data box
#            data = table.findAll('span', {'class': 'txt7'})

#            # The URL
#            committee_url = table.find('a', {'class': 'sublink2'})
#            item.add_value("url", urljoin("http://cal-access.sos.ca.gov", committee_url['href']))

#            # The name
#            committee_name = committee_url.text
#            item.add_value("name", committee_name)

#            # ID sometimes refers to xref_filer_id rather than filer_id_raw
#            committee_id = data[0].text
#            item.add_value("id", committee_id)

#            # Does the committee support or oppose the measure?
#            committee_position = data[1].text.strip()
#            item.add_value("position", committee_position)

#            # Load it
#            yield item.load_item()
