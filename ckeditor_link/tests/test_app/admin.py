from django import forms
from django.contrib import admin
from django.db import models
from django.forms import DateTimeInput

from ckeditor_link.admin import DjangoLinkAdmin

from .models import TestModel, LinkModel


class LinkModelForm(forms.ModelForm):
    when = forms.DateField(widget=forms.SelectDateWidget, required=False)


class LinkAdmin(DjangoLinkAdmin):
    form = LinkModelForm

admin.site.register(TestModel)
admin.site.register(LinkModel, LinkAdmin)
