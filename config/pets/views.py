from django.shortcuts import render, redirect
from .models import Pet
from django.contrib.auth.decorators import login_required
from . import forms


# Create your views here.
def pets_list(request):
    pets = Pet.objects.all().order_by('-date')
    return render(request, 'pets/pets_list.html', {'pets': pets})
def pet_page(request, slug):
    pet = Pet.objects.get(slug=slug)
    return render(request, 'pets/pet_page.html', {'pet': pet})

@login_required(login_url='/users/sign_in/')
def pet_new(request):
    if request.method == 'POST':
        form = forms.SurrenderPet(request.POST, request.FILES)
        if form.is_valid():
            new_surrender_form = form.save(commit=False)
            new_surrender_form.owner = request.user
            new_surrender_form.save()
            # needs to be changed- now is redirecting directly to the Adopt a Pet section,
            # without beeing approved by admin
            return redirect('pets:list')
    else:
        form = forms.SurrenderPet()
    return render(request, 'pets/pet_new.html', {'form': form})


