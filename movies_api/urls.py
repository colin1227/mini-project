from django.urls import path
from .views import Movies, Movie_Detail

urlpatterns = [
    path('', Movies.as_view()),
    path('<int:pk>/', Movie_Detail.as_view()),
]