from django.urls import path

from .views import EntryView

urlpatterns = [
    path('', EntryView.as_view(), name='veterinary'),
    # path('ask/', AskView.as_view(), name='ask'),
]