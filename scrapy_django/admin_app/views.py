from django.shortcuts import render

# Create your views here.

def register_page(request):
    return render(request, 'admin_pages/register.html')

def login_page(request):
    return render(request, 'admin_pages/login.html')

