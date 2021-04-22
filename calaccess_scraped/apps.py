#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic configuration for the application.
"""
from django.apps import AppConfig


class CalAccessScrapedConfig(AppConfig):
    """
    Application configuration.
    """
    name = 'calaccess_scraped'
    verbose_name = "CAL-ACCESS scraped data"
    default_auto_field = 'django.db.models.BigAutoField'
