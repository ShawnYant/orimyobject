from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User

from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.

def index(request):
    return render(request,'myadmin/index/index.html')

#administrator login form:
def login(request):
    return render(request,'myadmin/index/login.html')

#perform the login
def dologin(request):
    try:
        if request.POST['code'] != request.session['verifycode']:
             context = {"info_login":"Verification Code Error!"}
             return render(request,"myadmin/index/login.html",context)



        #Obtain user information based on login account
        user = User.objects.get(username=request.POST['username'])
        Word = request.POST['pass']
        #Check whether the current user is an administrator
        if user.status == 6:
            #identify whether the password is valid
            # import hashlib
            # md5 = hashlib.md5()
            # s = request.POST['pass']+user.password_salt #Get the password from the form and add an interference value
            # md5.update(s.encode('utf-8')) 
            if Word == user.password :#get the value of MD5
                print('login successfully!')
                request.session['adminuser'] = user.toDict()
                return redirect(reverse('myadmin_index'))
            else:
                context = {"info_login":"Incorrect login password!"}

        else :
            context = {"info_login":"Invalid Account!"}
    except Exception as err:
        print(err)
        context = {"info_login":"The login account does not exist!"}
    return render(request,"myadmin/index/login.html",context)

#exit
def logout(request):
    del request.session['adminuser']
    return redirect(reverse('myadmin_login'))

def verify(request):
    #Output verification code
    import random
    from PIL import Image, ImageDraw, ImageFont
   
    bgcolor = (242,164,247)
    width = 100
    height = 25
   
    im = Image.new('RGB', (width, height), bgcolor)
    
    draw = ImageDraw.Draw(im)
  
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
  
    str1 = '0123456789'
 
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
  
    font = ImageFont.truetype('static/arial.ttf', 21)
  
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
 
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
  
    del draw

    request.session['verifycode'] = rand_str
 
   
    import io
    buf = io.BytesIO()
  
    im.save(buf, 'png')
    
    return HttpResponse(buf.getvalue(), 'image/png')
    