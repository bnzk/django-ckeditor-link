# compat
import django
from django import forms
from django.contrib import admin

from ckeditor_link.admin import DjangoLinkAdmin

from .models import CMSFilerLinkModel, ContribLinkModel, LinkModel, TestModel

if django.VERSION[:2] < (1, 10):
    from django.forms.extras.widgets import SelectDateWidget
else:
    from django.forms.widgets import SelectDateWidget


class LinkModelForm(forms.ModelForm):
    when = forms.DateField(widget=SelectDateWidget, required=False)


admin.site.register(TestModel)


@admin.register(LinkModel)
class CKLinkModelAdmin(DjangoLinkAdmin):
    form = LinkModelForm


@admin.register(ContribLinkModel)
class CKBaseLinkModelAdmin(DjangoLinkAdmin):
    pass


@admin.register(CMSFilerLinkModel)
class CMSFilerCKLinkModelAdmin(DjangoLinkAdmin):
    pass
