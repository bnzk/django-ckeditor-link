from django.contrib import admin

from ckeditor_link.admin import ckeditor_linkMixin
from models import TestModelSingle, TestModelAdvanced, TestModelInInlineModel, TestInlineModelSingle, \
    TestInlineModel


class TestModelAdmin(ckeditor_linkMixin, admin.ModelAdmin):
    single_formfield_stash = ('selection', )

admin.site.register(TestModelSingle, TestModelAdmin)


class TestInlineModelInline(admin.StackedInline):
    model = TestInlineModel


ADVANCED_STASH = {
    'set': {
        'set1': ('set1_1', '#testinlinemodel_set-group', ),
        'set2': ('set2_1', 'set2_2', 'set2_3', ),
        'set3': ('set3_1', 'set2_1', ),
    },
}


class TestModelAdvancedAdmin(ckeditor_linkMixin, admin.ModelAdmin):
    inlines = [TestInlineModelInline, ]
    formfield_stash = ADVANCED_STASH

admin.site.register(TestModelAdvanced, TestModelAdvancedAdmin)


class TestInlineModelSingleInline(ckeditor_linkMixin, admin.StackedInline):
    model = TestInlineModelSingle
    single_formfield_stash = ('selection', )


class TestModelInInlineModelAdmin(ckeditor_linkMixin, admin.ModelAdmin):
    inlines = [TestInlineModelSingleInline, ]

admin.site.register(TestModelInInlineModel, TestModelInInlineModelAdmin)
