from django.urls import path

from . import views

urlpatterns = [
    path('test_ws/', views.test_ws, name='test_ws'),
]