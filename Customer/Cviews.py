from urllib import request
from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from Customer import models
from Customer.forms import RegisterForm

from Customer.models import UserForm


def index(request):
    pass
    return render(request,'web/index.html')

def login(request):
     if request.session.get('is_login',None):
        return redirect('web/index')

     if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Please check again"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "incorrect password"
            except:
                message = "User do not exist"
        return render(request, '\web\login.html', locals())

     login_form = UserForm()
     return render(request, 'web\login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect("\web\index.html")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "please check！"
        if register_form.is_valid():  
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  
                message = "password do not match"
                return render(request, 'web\ regis.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  
                    message = 'Choose another name please, its been taken！'
                    return render(request, 'web\ regis.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  
                    message = 'This email is in use！'
                    return render(request, 'web\ regis.html', locals())

                
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('web\login.html')  
    register_form = RegisterForm()
    return render(request, 'web\ regis.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
       return redirect("web\index.html")
    request.session.flush()
    # 
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("web\index.html")