from django.shortcuts import render

# Create your views here.

def main_page(request):
    return render(request, 'job_pages/main.html')

def introduce_page(request):
    return render(request, 'job_pages/introduce.html')

def menu_page(request):
    return render(request, 'job_pages/menu.html')