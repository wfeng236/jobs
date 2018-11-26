
from django.shortcuts import render,HttpResponse

# Create your views here.

#跳转用户注册页面
def register_page(request):
    return render(request, 'admin_pages/register.html')






















def login_page(request):
    return render(request, 'admin_pages/login.html')

