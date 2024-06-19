from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def sign_up_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pets:list')
    else:
        form = UserCreationForm()
    return render(request, 'users/sign_up.html', { 'form': form })

