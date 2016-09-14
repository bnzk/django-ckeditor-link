from django.views.generic import DetailView

from .models import TestModel


class TestModelDetailView(DetailView):
    model = TestModel
