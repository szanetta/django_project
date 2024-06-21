from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.pets_list, name='list'),
    path('new-pet/', views.pet_new, name='new-pet'),
    path('/<slug:slug>', views.pet_page, name='page'),
    path('pet-approval/', views.pet_approval, name='approval'),
]