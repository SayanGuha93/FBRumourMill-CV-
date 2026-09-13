from django.urls import path

from . import views


urlpatterns = [
    path("clubs/", views.ClubListCreateView.as_view()),
    path("clubs/<int:pk>/", views.ClubDetailView.as_view()),

    path("players/", views.PlayerListCreateView.as_view()),
    path("players/<int:pk>/", views.PlayerDetailView.as_view()),

    path("transfer-rumours/", views.TransferRumourListCreateView.as_view()),
    path("transfer-rumours/<int:pk>/", views.TransferRumourDetailView.as_view()),
]