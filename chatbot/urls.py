from django.urls import path

from .views import AskView, EntryView

urlpatterns = [
    path('', EntryView.as_view(), name='chatbot'),
    path('ask/', AskView.as_view(), name='ask'),
]