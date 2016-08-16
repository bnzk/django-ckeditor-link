from django.contrib import admin

from .models import TestModel, LinkModel

admin.site.register(TestModel)
admin.site.register(LinkModel)
