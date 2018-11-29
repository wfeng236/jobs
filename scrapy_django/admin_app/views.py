import datetime
import os
import random
import string
import traceback

from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect

from admin_app.captcha.image import ImageCaptcha
from admin_app.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from admin_app import utils

# Create your views here.




#跳转用户注册页面
def register_page(request):
    request.session['email_status']='0'
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

# 异步验证手机号
def ajax_phone(request):
    phone = request.POST.get("phone")
    print(phone)
    if phone == None:
        return HttpResponse('2')
    elif User.objects.filter(phone=phone):
        return HttpResponse("0")
    else:
        return HttpResponse("1")


#异步发送验证码
def ajax_emailyz(request):
    email = request.GET.get('email')
    print(email)
    subject, from_email, to = '请您完成验证(24小时有效)！', 'niuniu837365144@sina.com',email
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册<a href="http://127.0.0.1:8000/user/register/emailyz/" target=blank>www.niubiyouxiang.com</a>，\欢迎你来验证你的邮箱，验证结束你就可以登录了！</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse('1')

#跳转用户邮箱验证页面
def register_emailyz(request):
    request.session['email_status']='1'
    username = request.GET.get('username')
    flag = request.GET.get('flag')
    print(flag)
    return render(request,'admin_pages/emailyz.html',{'username':username,'flag':flag})

#注册接收
def register_logic(request):
    dict_1 = {
        '0':'9',
        '1':'8',
        '2':'7',
        '3':'6',
        '4':'5',
        '5':'4',
        '6':'3',
        '7':'2',
        '8':'1',
        '9':'0'
    }
    try:
        #获取用户输入的邮箱/手机号码
        username = request.POST.get("username")
        #获取用户输入的手机号
        phone = request.POST.get('phone')
        #获取用户对应的id
        user_id = ''
        for i in phone:
            user_id += dict_1[i]
        #获取用户的邮箱
        email = request.POST.get('email')
        #获取用户输入的第一次密码
        password1 = request.POST.get("password")
        #获取用户输入的第二次密码
        password2 = request.POST.get("password2")
        #随机盐
        salt = utils.getSalt()
        #随机盐和密码拼接
        password = utils.hashCode(password2,salt=salt)
        #注册时间
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #获取邮箱验证状态
        email_status = request.session.get('email_status')
        if email_status == '1':
            status = 1
        else:
            status = 0
        print(user_id,username,password,phone,email,salt,time,status)
        with transaction.atomic():
            if username and phone and email and password1 == password2:
                User(user_id=user_id, username=username, password=password, phone=phone, email=email, salt=salt,
                     time=time, status=status).save()
                if status == 0:
                    return HttpResponse('5')
                else:
                    return HttpResponse('6')
            #             else:
            #                 return HttpResponse('0000')
            #         else:
            #             return HttpResponse('000')
            #     else:
            #         return HttpResponse('00')
            # else:
            #     return HttpResponse('0')
    except:
        traceback.print_exc()
        #注册失败重新回到注册页面
        return redirect("user:register:page")

#登录跳转页面
def login_page(request):
    # 获取用户对象
    username = request.GET.get('username')
    database_user = User.objects.filter(username=username)
    print(database_user)
    if database_user:
        database_user[0].status = 1
        database_user[0].save()
    return render(request, 'admin_pages/login.html')

#生成验证码
def get_captcha(request):
    #1.创建一个ImageCaptcha对象
    cap = ImageCaptcha(fonts=[os.path.abspath("captcha/font/simhei.ttf")])
    #获取4位随机验证码值
    code_list = random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,4)
    code = ''.join(code_list)
    #3.将验证码存入session
    request.session["code"]=code
    print(code)
    #4.生成验证码图片
    data = cap.generate(code)
    #5.写出图片
    return HttpResponse(data,"image/png")

#异步验证登录验证码
def ajax_yzm(request):
    '''
    接收ajax请求
    :param request:
    :return:
    '''

    #1.获取真实的码
    realcode = request.session.get("code")
    print(realcode)
    #2.获取用户输入码
    usercode = request.POST.get("usercode")
    print(usercode)
    #判断验证码
    if realcode.lower() == usercode.lower():
        return HttpResponse("1")
    else:
        return HttpResponse("0")

#登录接收页面
def login_logic(request):
    try:
        #获取用户名
        username=request.POST.get("username")
        #获取用户密码
        password=request.POST.get("password")
        #获取用户对象
        database_user = User.objects.filter(username=username)
        print(username,password)
        #获取真实的验证码
        realcode=request.session.get("code")
        #2.获取用户输入码
        usercode=request.POST.get("usercode")
        with transaction.atomic():
            if realcode.lower() == usercode.lower():
                # 如果对象存在-
                if database_user:
                    # 获取用户邮箱验证状态
                    email_status = database_user[0].status
                    # 拿到对象盐值加密的密码
                    database_password = database_user[0].password
                    # 拿到盐
                    salt = database_user[0].salt
                    # 将新输入的密码盐值重新哈希加密
                    password_1 = utils.hashCode(password, salt=salt)
                    if User.objects.filter(username=username, password=password_1):
                        if email_status == '1':
                            # 将用户名存入session
                            request.session['login_user'] = username
                            return HttpResponse('6')
                        else:
                            return HttpResponse('000')
                    else:
                        return HttpResponse('00')
                else:
                    return HttpResponse('00')
            else:
                return HttpResponse('0')

    except:
        traceback.print_exc()
        #登录失败重新回到注册页面
        return redirect("user:login:page")

