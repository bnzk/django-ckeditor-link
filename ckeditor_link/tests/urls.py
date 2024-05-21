"""URLs to run the tests."""

from django.contrib import admin
from django.urls import include, path

from ckeditor_link.tests.test_app.views import TestModelDetailView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("testmodel/<int:pk>/", TestModelDetailView.as_view(), name="testmodel_detail"),
    path("", include("cms.urls")),
]

# if settings.DEBUG:
#     urlpatterns += [
#         url(
#             r"^media/(?P<path>.*)$",
#             "django.views.static.serve",
#             {"document_root": settings.MEDIA_ROOT},
#         ),
#     ]
