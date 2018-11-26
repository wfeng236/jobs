
from django.shortcuts import render,HttpResponse
from admin_app.models import User
# Create your views here.




#跳转用户注册页面
def register_page(request):
    return render(request, 'admin_pages/register.html')

#异步验证用户名
def ajax_username(request):
    username = request.POST.get("username")
    print(username)
    if username == None:
        return HttpResponse('2')
    elif User.objects.filter(username=username):
        return HttpResponse("0")
    else:
        return HttpResponse("1")





















def login_page(request):
    return render(request, 'admin_pages/login.html')

