from django import forms
from django.contrib import admin
from django.forms.extras.widgets import SelectDateWidget

from ckeditor_link.admin import DjangoLinkAdmin

from .models import TestModel, LinkModel


class LinkModelForm(forms.ModelForm):
    when = forms.DateField(widget=SelectDateWidget, required=False)


class CKLinkModelAdmin(DjangoLinkAdmin):
    form = LinkModelForm

admin.site.register(TestModel)
admin.site.register(LinkModel, CKLinkModelAdmin)
