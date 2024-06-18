from django.shortcuts import render
from .models import Pet


# Create your views here.
def pets_list(request):
    pets = Pet.objects.all().order_by('-date')
    return render(request, 'pets/pets_list.html', {'pets': pets})
def pet_page(request, slug):
    pet = Pet.objects.get(slug=slug)
    return render(request, 'pets/pet_page.html', {'pet': pet})




