from django import forms
from django.contrib import admin
from django.db import models
from django.forms import DateTimeInput

from ckeditor_link.admin import DjangoLinkAdmin

from .models import TestModel, CKLinkModel


class CKLinkModelForm(forms.ModelForm):
    when = forms.DateField(widget=forms.SelectDateWidget, required=False)


class CKLinkModelAdmin(DjangoLinkAdmin):
    form = CKLinkModelForm

admin.site.register(TestModel)
admin.site.register(CKLinkModel, CKLinkModelAdmin)
