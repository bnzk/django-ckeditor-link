from django.conf.urls import url
from django.contrib import admin
from django.db import models
from django.http import JsonResponse


class DjangoLinkAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        """
        http://stackoverflow.com/questions/2431727/django-admin-hide-a-model
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def get_urls(self):
        """
        add verify url.
        """
        my_urls = [
            url(
                r'^verify/$',
                self.admin_site.admin_view(self.verify),
                name=self._get_verify_url_name()
            ),
        ]
        return my_urls + super(DjangoLinkAdmin, self).get_urls()

    def _get_verify_url_name(self):
        return '{0}_{1}_verify'.format(self.model._meta.app_label,
                                       self.model._meta.model_name)

    def verify(self, request):
        """
        verify data with modelform, send through data.
        :param request:
        :return:
        """
        form = self.get_form(request, )(request.POST)
        if form.is_valid():
            verified_data = form.cleaned_data
            obj = self.model(**verified_data)
            link_value = ''
            # prepopulate href
            if (getattr(obj, 'get_link', None)):
                link_value = obj.get_link()
            # basic serialize only
            for key, value in verified_data.items():
                if isinstance(value, models.Model):
                    verified_data[key] = value.id
            return_data = {"valid": 'true', 'data': verified_data, 'link_value': link_value}
        else:
            errors = form.errors
            return_data = {"valid": 'false', 'errors': errors}
        return JsonResponse(return_data)

    def save_model(self, request, obj, form, change):
        """
        no save!
        """
        return False
