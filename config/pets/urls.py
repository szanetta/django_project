from django.urls import path
from . import views

app_name = 'pets'

urlpatterns = [
    path('', views.pets_list, name='list'),
    path('new-pet/', views.pet_new, name='new-pet'),
    path('/<slug:slug>', views.pet_page, name='page'),
    path('pet-approval-list/', views.pets_approval_list, name='pets-approval-list'),
    path('pet-approval-page/<slug:slug>', views.pet_approval_page, name='pet-approval-page'),
]