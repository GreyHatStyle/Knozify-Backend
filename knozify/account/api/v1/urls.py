from django.urls import path

from . import views

urlpatterns = [
    path('first/', views.FirstAPI.as_view(), name='first'),
]
