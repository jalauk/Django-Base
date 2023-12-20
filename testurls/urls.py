from django.urls import path
from .views import TestView

urlpatterns = [
    path("testurl", TestView.as_view())
]
