#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
General utilities for the application.
"""
import os
default_app_config = 'calaccess_scraped.apps.CalAccessScrapedConfig'


def get_data_directory():
    """
    Returns directory for scraped data.
    """
    return os.path.join(os.path.dirname(__file__), 'data')
