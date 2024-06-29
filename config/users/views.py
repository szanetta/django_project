from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from pets.models import Pet

from .forms import CustomUserCreationForm
def sign_up_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pets:list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/sign_up.html', {'form': form})

def sign_in_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('pets:list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/sign_in.html', {'form': form})

def sign_out_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('pets:list')

@login_required(login_url='/users/sign_in/')
def user_pets_list(request):
    user = request.user
    user_pets = Pet.objects.filter(owner=user).order_by('-date')
    return render(request, 'pets/user_pets_list.html', {'user_pets': user_pets})