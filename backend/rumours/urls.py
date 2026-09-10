from django.urls import path
from .views import RumourListCreateView, RumourDetailView


urlpatterns = [
    path("", RumourListCreateView.as_view(), name="rumour-list-create"),
    path("<int:pk>/", RumourDetailView.as_view(), name="rumour-detail"),
]