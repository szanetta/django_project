from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.pets_list, name='list'),
    path('/<slug:slug>', views.pet_page, name='page'),
]