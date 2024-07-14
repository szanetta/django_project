from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet, Application
from .forms import ApplicationForm
from django.contrib import messages
from django.urls import reverse

def pets_list(request):
    pets = Pet.objects.filter(approved=True).order_by('-date')
    return render(request, 'pets/pets_list.html', {'pets': pets})
def pet_page(request, slug):
    pet = get_object_or_404(Pet, slug=slug)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            applicant_email = form.cleaned_data['applicant_email']
            message = form.cleaned_data['message']
            Application.objects.create(pet=pet, applicant_email=applicant_email, message=message)

            return redirect('pets:application_submitted', pet_slug=pet.slug)
    else:
        form = ApplicationForm()

    context = {
        'pet': pet,
        'form': form,
    }
    return render(request, 'pets/pet_page.html', context)

@login_required(login_url='/users/sign_in/')
def pet_new(request):
    if request.method == 'POST':
        form = forms.SurrenderPet(request.POST, request.FILES)
        if form.is_valid():
            new_surrender_form = form.save(commit=False)
            new_surrender_form.owner = request.user
            new_surrender_form.save()
            messages.success(request,"Thank you for submiting the form. Your surrender application is awaiting approval.")
            if not request.user.is_superuser:
                return redirect('pets:new-pet')
            else:
                return redirect('pets:pets-approval-list')
    else:
        form = forms.SurrenderPet()
    return render(request, 'pets/pet_new.html', {'form': form})


def pets_approval_list(request):
    pets_awaiting_list = Pet.objects.all().order_by('-date')
    return render(request,'pets/pets_approval_list.html', {'pets_awaiting_list': pets_awaiting_list})

def pet_approval_page(request, slug):
    pet_awaiting_page = Pet.objects.get(slug=slug)
    if request.method == "POST":
        data = request.POST
        if 'approved' in data:
            pet_awaiting_page.approved = True
            pet_awaiting_page.save()
            return redirect('pets:pets-approval-list')
        elif 'rejected' in data:
            pet_awaiting_page.rejected = True
            pet_awaiting_page.save()

    return render(request, 'pets/pet_approval_page.html', {'pet_awaiting_page': pet_awaiting_page})


def apply_for_adoption(request, slug):
    pet = get_object_or_404(Pet, slug=slug)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.pet = pet
            application.save()
            return redirect('pets:application_submitted', pet_slug=pet.slug)
    else:
        form = ApplicationForm()

    context = {
        'form': form,
        'pet': pet,
    }
    return render(request, 'pets/pet_page.html', context)

def application_submitted(request, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    return render(request, 'pets/application_submitted.html', {'pet': pet})

def remove_pet(request, slug):
    pet = get_object_or_404(Pet, slug=slug)

    if pet.owner != request.user:
        messages.error(request, "You are not authorized to delete this pet.")
        return redirect('pets:list')

    if request.method == 'POST':
        pet.delete()
        messages.success(request, f"{pet.name} has been successfully deleted.")
        return redirect('pets:user_pets_list')  # Przekierowanie do listy zwierząt użytkownika

    context = {
        'pet': pet
    }
    return render(request, 'pets/remove_pet.html', context)

#@login_required(login_url='/users/sign_in/') path('sign_in/', views.sign_in_view, name='sign_in'),
@login_required(login_url='sign_in')
def user_pets_list(request):
    user = request.user
    user_pets = Pet.objects.filter(owner=user).order_by('-date')
    return render(request, 'pets/user_pets_list.html', {'user_pets': user_pets})