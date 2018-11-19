from django.urls import path
from .views import Movie

urlpatterns = [
    path('', Movie.as_view()),
    #path('<int:pk>/', Movie_detail.as_view()),
]