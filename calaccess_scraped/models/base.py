#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base models for storing information scraped from the CAL-ACCESS website.
"""
from __future__ import unicode_literals
import textwrap
from django.db import models
from django.db.models.base import ModelBase
from django.template.defaultfilters import capfirst


class CalAccessMetaClass(ModelBase):
    """
    A custom metaclass for our base model.

    Automatically configures Meta attributes common to all models.
    """
    def __new__(cls, name, bases, attrs):
        """
        Override the default __new__ behavior.
        """
        klass = super(CalAccessMetaClass, cls).__new__(cls, name, bases, attrs)

        # Cook up an automated verbose name for each model
        klass_str = str(klass).replace("<class 'calaccess_scraped.models.", "")
        klass_group = klass_str.split(".")[0].upper()
        klass_table = capfirst(klass._meta.verbose_name_plural)
        klass_name = "{0}: {1}".format(klass_group, klass_table)

        # Insert the verbose name into each model's configuration
        klass._meta.verbose_name = klass_name
        klass._meta.verbose_name_plural = klass_name

        # Set the app_label too
        klass._meta.app_label = "calaccess_scraped"

        # Finish up
        return klass


class CalAccessBaseModel(models.Model):
    """
    An abstract model with some tricks we'll reuse.
    """
    __metaclass__ = CalAccessMetaClass

    def doc(self):
        """
        Return the model's docstring as a readable string ready to print.
        """
        if self.__doc__.startswith(self.klass_name):
            return ''
        return textwrap.dedent(self.__doc__).strip()

    @property
    def db_table(self):
        """
        Return the model's database table name as a string.
        """
        return self._meta.db_table

    @property
    def klass(self):
        """
        Return the model class itself.
        """
        return self.__class__

    @property
    def klass_name(self):
        """
        Return the name of the model class.
        """
        return self.__class__.__name__

    @property
    def klass_group(self):
        """
        Return the name of the model's group, as determined by its submodule.
        """
        return str(self.__class__).split(".")[-2]

    def get_field_list(self):
        """
        Return all the fields on the model as a list.
        """
        return self._meta.fields

    class Meta:
        """
        Meta model options.
        """
        abstract = True
        app_label = 'calaccess_scraped'


class BaseScrapedModel(CalAccessBaseModel):
    """
    Abstract base model from which all scraped models inherit.
    """
    url = models.URLField(max_length=2000, null=True)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Model options.
        """
        abstract = True


class BaseScrapedElection(BaseScrapedModel):
    """
    An election day scraped from the California Secretary of State's site.

    This is an abstract base model that creates two tables, one for elections
    scraped as part of the candidates scraper, and one for elections scraped
    as part of the propositions scraper.
    """
    name = models.CharField(max_length=200)

    class Meta:
        """
        Model options.
        """
        abstract = True


class BaseScrapedCommittee(BaseScrapedModel):
    """
    An committee scraped from the California Secretary of State's site.

    This is an abstract base model that creates two tables, one for committees
    scraped as part of the candidates scraper, and one for committees scraped
    as part of the propositions scraper.
    """
    name = models.CharField(
        verbose_name="committee name",
        max_length=500
    )
    scraped_id = models.CharField(
        verbose_name="committee identification number",
        max_length=7
    )

    class Meta:
        """
        Model options.
        """
        abstract = True
