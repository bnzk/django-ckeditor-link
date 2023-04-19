"""URLs to run the tests."""
from django.conf.urls import include
from django.urls import path, re_path
from django.contrib import admin

from ckeditor_link.tests.test_app.views import TestModelDetailView


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^testmodel/(?P<pk>\d+)/$', TestModelDetailView.as_view(), name='testmodel_detail'),
    path('', include('cms.urls')),
]

# if settings.DEBUG:
#     urlpatterns += [
#         url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
#     ]
