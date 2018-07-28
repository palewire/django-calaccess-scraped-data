#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base classes for custom management commands.
"""
import os
import re
import logging
import requests
from itertools import cycle
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils import timezone
from six.moves.urllib.parse import urljoin
from django.utils.termcolors import colorize
from calaccess_scraped.decorators import retry
from six.moves.urllib.request import url2pathname
from django.core.management.base import BaseCommand
from calaccess_scraped.models.tracking import ScrapedDataVersion
logger = logging.getLogger(__name__)


class CalAccessCommand(BaseCommand):
    """
    Base class for all custom CalAccess-related management commands.
    """
    def handle(self, *args, **options):
        """
        Sets options common to all commands.

        Any command subclassing this object should implement its own
        handle method, as is standard in Django, and run this method
        via a super call to inherit its functionality.
        """
        # Set global options
        self.verbosity = options.get("verbosity")
        self.no_color = options.get("no_color")

        # Start the clock
        self.start_datetime = timezone.now()

    def header(self, string):
        """
        Writes out a string to stdout formatted to look like a header.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="cyan", opts=("bold",))
        self.stdout.write(string)

    def log(self, string):
        """
        Writes out a string to stdout formatted to look like a standard line.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize("%s" % string, fg="white")
        self.stdout.write(string)

    def success(self, string):
        """
        Writes out a string to stdout formatted green to communicate success.
        """
        logger.debug(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="green")
        self.stdout.write(string)

    def warn(self, string):
        """
        Writes string to stdout formatted yellow to communicate a warning.
        """
        logger.warn(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="yellow")
        self.stdout.write(string)

    def failure(self, string):
        """
        Writes string to stdout formatted red to communicate failure.
        """
        logger.error(string)
        if not getattr(self, 'no_color', None):
            string = colorize(string, fg="red")
        self.stdout.write(string)

    def duration(self):
        """
        Calculates how long command has been running and writes it to stdout.
        """
        duration = timezone.now() - self.start_datetime
        self.stdout.write('Duration: {}'.format(str(duration)))
        logger.debug('Duration: {}'.format(str(duration)))

    def __str__(self):
        return re.sub(r'(.+\.)*', '', self.__class__.__module__)


class ScrapeCommand(CalAccessCommand):
    """
    Base management command for scraping the CAL-ACCESS website.
    """
    base_url = 'http://cal-access.sos.ca.gov/'
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
            '--force-download',
            action='store_true',
            dest='force_download',
            default=False,
            help='Force the scraper to download URLs even if they are cached',
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
        super(ScrapeCommand, self).handle(*args, **options)

        self.force_flush = options.get("force_flush")
        self.force_download = options.get("force_download")
        self.update_cache = options.get("update_cache")

        os.path.exists(self.cache_dir) or os.mkdir(self.cache_dir)

    def get_scraped_version(self):
        """
        Get or create the current processed version.

        Return a tuple (ProcessedDataVersion object, created), where
        created is a boolean specifying whether a version was created.
        """
        return ScrapedDataVersion.objects.create()


class ScrapePageCommand(ScrapeCommand):
    """
    Base management command for scraping a page/subsection of the CAL-ACCESS website.
    """
    def handle(self, *args, **options):
        """
        Make it happen.
        """
        super(ScrapePageCommand, self).handle(*args, **options)

        # Verify cache directory exists
        os.path.exists(self.cache_dir) or os.mkdir(self.cache_dir)

        # Flush if requested
        if self.force_flush:
            self.flush()

        # Fetch a list of proxy addresses and user agents
        self.proxy_pool = cycle(self.get_proxies())
        self.useragent_list = [
             # Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            # Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
        ]
        self.useragent_pool = cycle(self.useragent_list)

        # Scrape the data
        results = self.scrape()

        # Save the results
        self.save(results)

    def get_proxies(self):
        """
        Fetch a list of proxy addresses from the web.
        """
        # Fetch the page with the list
        r = requests.get('https://free-proxy-list.net/')

        # Set it up in BeautifulSoup for parsing
        soup = BeautifulSoup(r.text, "html.parser")

        # Initialize a blank list to use later
        proxies = set()

        # Loop through all the rows in the table we want to scrape
        for row in soup.find("tbody").find_all('tr')[:25]:

            # If it is listed as a working proxy ...
            if 'yes' in str(row):
                # ... parse out the IP
                cell_list = row.find_all("td")
                ip = cell_list[0].string
                port = cell_list[1].string

                # Add it to our list
                proxies.add("{}:{}".format(ip, port))

        # Return the list
        return proxies

    @retry((requests.exceptions.RequestException, requests.exceptions.ReadTimeout))
    def get_url(self, url, retries=1, request_type='GET'):
        """
        Returns the response from a URL, retries if it fails.
        """
        # Set the headers
        headers = {
            'User-Agent': next(self.useragent_pool),
        }

        # Set the proxy
        proxy = next(self.proxy_pool)
        proxies = {
            "http": proxy,
            "https": proxy
        }

        # Log, if that's what we want to do
        if self.verbosity > 2:
            self.log(" Making a {} request for {} with proxy {}".format(request_type, url, proxy))

        # Make the request and return the result
        return getattr(requests, request_type.lower())(
            url,
            headers=headers,
            proxies=proxies,
            timeout=5
        )

    def get_headers(self, url):
        """
        Returns a dict with metadata about the current CAL-ACCESS snapshot.
        """
        response = self.get_url(url, request_type='HEAD')
        length = int(response.headers['content-length'])
        return {
            'content-length': length,
        }

    def get_html(self, url, retries=1, base_url=None):
        """
        Makes request for a URL and returns HTML as a BeautifulSoup object.
        """
        # Put together the full URL
        full_url = urljoin(base_url or self.base_url, url)
        if self.verbosity > 2:
            self.log(" Retrieving data for {}".format(url))

        # Pull a cached version of the file, if it exists
        cache_path = os.path.join(
            self.cache_dir,
            url2pathname(url.strip("/"))
        )
        if os.path.exists(cache_path) and not self.force_download:
            # Make a HEAD request for the file size of the live page
            if self.update_cache:
                cache_file_size = os.path.getsize(cache_path)
                head = self.get_headers(full_url)
                web_file_size = head['content-length']

                if self.verbosity > 2:
                    msg = " Cached file sized {}. Web file size {}."
                    self.log(msg.format(
                        cache_file_size,
                        web_file_size
                    ))

            # If our cache is the same size as the live page, return the cache
            if not self.update_cache or cache_file_size == web_file_size:
                if self.verbosity > 2:
                    self.log(" Returning cached {}".format(cache_path))
                html = open(cache_path, 'r').read()
                return BeautifulSoup(html, "html.parser")

        # Otherwise, retrieve the full page and cache it
        try:
            response = self.get_url(full_url)
        except requests.exceptions.HTTPError as e:
            # If web requests fails, fall back to cached file, if it exists
            if os.path.exists(cache_path):
                if self.verbosity > 2:
                    self.log(" Returning cached {}".format(cache_path))
                html = open(cache_path, 'r').read()
                return BeautifulSoup(html, "html.parser")
            else:
                raise e

        # Grab the HTML and cache it
        html = response.text
        if self.verbosity > 2:
            self.log(" Writing to cache {}".format(cache_path))
        cache_subdir = os.path.dirname(cache_path)
        os.path.exists(cache_subdir) or os.makedirs(cache_subdir)
        with open(cache_path, 'w') as f:
            f.write(html)

        # Finally return the HTML ready to parse with BeautifulSoup
        return BeautifulSoup(html, "html.parser")

    def flush(self):
        """
        This method should empty out database tables filled by this command.
        """
        raise NotImplementedError

    def scrape(self):
        """
        This method should perform the actual scraping.

        Returns the structured data.
        """
        raise NotImplementedError

    def save(self, results):
        """
        This method should process structured data returned by `build_results`.
        """
        raise NotImplementedError
