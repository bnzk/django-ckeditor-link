from django.contrib import admin
from django.db import models
from django.forms import DateTimeInput

from ckeditor_link.admin import DjangoLinkAdmin

from .models import TestModel, LinkModel


class LinkAdmin(DjangoLinkAdmin):
    pass

admin.site.register(TestModel)
admin.site.register(LinkModel, LinkAdmin)
