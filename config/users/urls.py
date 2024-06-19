from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('sign_in/', views.sign_in_view, name='sign_in'),
    path('sign_out/', views.sign_out_view, name='sign_out'),
]