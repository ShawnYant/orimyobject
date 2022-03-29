from django.shortcuts import redirect, render
from django.urls import reverse
from myadmin.models import User



def regist(request):
    errors=[]
    confirm_password=None
    username=None
    password=None
    email=None
    phone=None
    judge=False
    if request.method == 'POST':
        if not request.POST.get('username'):
            errors.append('pass')
        else:
            username = request.POST.get('username',False);
        if not request.POST.get('password'):
            errors.append('pass')
        else:
            password = request.POST.get('password',False);
        if not request.POST.get('confirm_password'):
            errors.append('pass')
        else:
            confirm_password = request.POST.get('confirm_password',False);
        if not request.POST.get('email'):
            errors.append('pass')
        else:
            email= request.POST.get('email',False);
        if not request.POST.get('phone'):
            errors.append('pass')
            phone = request.POST.get('phone',False);
        if not request.POST.get('address'):
            errors.append('pass')
        else:
            username = request.POST.get('address',False);

        if password == confirm_password:
            judge=True
        else:
            errors.append('passwords do not match')
        if username is not None and password is not None and confirm_password is not None and email is not None and phone is not None and judge:
            if User.objects.filter(username=username):
                errors.append('this name is done')
            elif User.objects.filter(email=email):
                errors.append('this email is used')
            else:
                 registAdd = User.objects.create(username=username,password=password,email=email,phone=phone)
                 errors.append('Nice！')

            regist.save()
    return render(request,'web\Regist.html', {'errors': errors})
    
    # return redirect(reverse('web_orderhome_login'))
