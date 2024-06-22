from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pet,Notification
from django.contrib.auth.decorators import login_required
from . import forms


# Create your views here.
def pets_list(request):
    pets = Pet.objects.filter(approved=True).order_by('-date')
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
            if not request.user.is_superuser:
                notification = Notification.objects.create(
                    user=request.user,
                    message="Thank you for submitting the form. Your surrender application is awaiting approval."
                )
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
