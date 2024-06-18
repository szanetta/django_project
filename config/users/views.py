from django.shortcuts import render

# Create your views here.
def sign_up_view(request):
    return render(request, 'users/sign_up.html')