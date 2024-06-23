from .models import Pet
from django.contrib.auth.decorators import login_required
from . import forms
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pet, Application
from .forms import ApplicationForm

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
            if not request.user.is_superuser:
                return redirect('pets:list')
            else: return redirect('pets:pets-approval-list')
    else:
        form = forms.SurrenderPet()
    return render(request, 'pets/pet_new.html', {'form': form})


def pets_approval_list(request):
    pets_awaiting_list = Pet.objects.all().order_by('-date')
    # if request.user.is_superuser:
    #     #here needs to be function for approval only for super user
    # else:
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