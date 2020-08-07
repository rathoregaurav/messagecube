"""
app URL Configuration
"""

from django.urls import path

from data_capturing_unit.views import LoadData, MessageSearch

urlpatterns = [
    path('load-data/', LoadData.as_view()),
    path('search/', MessageSearch.as_view())
]
