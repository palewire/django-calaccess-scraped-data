#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Models for tracking processing of CAL-ACCESS snapshots over time.
"""
from __future__ import unicode_literals
from django.db import models
from datetime import datetime


class ScrapedDataVersion(models.Model):
    """
    A version of CAL-ACCESS scraped data.
    """
    process_start_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time processing started',
        help_text='Date and time when the scraping started',
        default=datetime.now,
    )
    process_finish_datetime = models.DateTimeField(
        null=True,
        verbose_name='date and time update finished',
        help_text='Date and time when the scraping finished'
    )

    class Meta:
        """
        Meta model options.
        """
        app_label = 'calaccess_scraped'
        verbose_name = 'TRACKING: CAL-ACCESS scraped data version'
        ordering = ('-process_start_datetime',)
        get_latest_by = 'process_start_datetime'

    def __str__(self):
        return str(self.process_start_datetime)

    @property
    def update_completed(self):
        """
        Check if the database update to the version completed.

        Return True or False.
        """
        if self.process_finish_datetime:
            is_completed = True
        else:
            is_completed = False

        return is_completed

    @property
    def update_stalled(self):
        """
        Check if the database update to the version started but did not complete.

        Return True or False.
        """
        if self.process_start_datetime and not self.update_finish_datetime:
            is_stalled = True
        else:
            is_stalled = False

        return is_stalled
