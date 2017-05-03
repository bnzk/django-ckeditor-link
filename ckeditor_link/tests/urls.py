"""URLs to run the tests."""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from ckeditor_link.tests.test_app.views import TestModelDetailView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^testmodel/(?P<pk>\d+)/$', TestModelDetailView.as_view(), name='testmodel_detail'),
]

# if settings.DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#     ]
