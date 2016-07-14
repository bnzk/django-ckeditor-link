from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models


SELECTION_CHOICES = (
    ('', 'Empty'),
    ('horse', 'Horse'),
    ('bear', 'Bear'),
    ('octopus', 'Octopus'),
)


SET_CHOICES = (
    ('', 'Empty'),
    ('set1', '1'),
    ('set2', '2'),
    ('set3', '3'),
)


@python_2_unicode_compatible
class TestModelSingle(models.Model):
    selection = models.CharField('Selection', max_length=20, blank=True, choices=SELECTION_CHOICES)
    horse = models.CharField(max_length=20, blank=True, )
    bear = models.CharField(max_length=20, blank=True, )
    octopus = models.CharField(max_length=20, blank=True, )

    def __str__(self):
        return "Single Stash Test Model: %s" % self.selection


@python_2_unicode_compatible
class TestModelAdvanced(models.Model):
    set = models.CharField('Selection', max_length=20, blank=True, choices=SET_CHOICES)
    set1_1 = models.CharField(max_length=20, blank=True, )
    set2_1 = models.CharField(max_length=20, blank=True, )
    set2_2 = models.CharField(max_length=20, blank=True, )
    set2_3 = models.CharField(max_length=20, blank=True, )
    set3_1 = models.CharField(max_length=20, blank=True, )

    def __str__(self):
        return "Test Model: %s" % self.set


@python_2_unicode_compatible
class TestInlineModel(models.Model):
    parent = models.ForeignKey(TestModelAdvanced)
    title = models.CharField(max_length=20, blank=True, )

    def __str__(self):
        return "A Simple Inline Model: %s" % self.title


@python_2_unicode_compatible
class TestModelInInlineModel(models.Model):
    title = models.CharField(max_length=20, blank=True, )

    def __str__(self):
        return "Has Stash In Inline Model: %s" % self.title


@python_2_unicode_compatible
class TestInlineModelSingle(models.Model):
    parent = models.ForeignKey(TestModelInInlineModel)
    selection = models.CharField('Selection', max_length=20, blank=True, choices=SELECTION_CHOICES)
    horse = models.CharField(max_length=20, blank=True, )
    bear = models.CharField(max_length=20, blank=True, )
    octopus = models.CharField(max_length=20, blank=True, )

    def __str__(self):
        return "Inline Stash Model: %s" % self.selection
