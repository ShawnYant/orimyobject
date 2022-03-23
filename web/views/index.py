from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import User,Category,Product


# Create your views here.

def index(request):
    ''' Ordering System Homepage'''
   
    clist = Category.objects.filter(status=1)
    categorylist = dict() 
    productlist = dict() 
  
    for vo in clist:
        c = {'id':vo.id,'name':vo.name,'pids':[]}
        plist = Product.objects.filter(category_id=vo.id,status=1)
       
        for p in plist:
            c['pids'].append(p.toDict())
            productlist[p.id]=p.toDict()
        categorylist[vo.id] = c   
        
    request.session['categorylist'] = categorylist
    request.session['productlist'] = productlist
    context = {'categorylist':request.session.get("categorylist",{}).items()}

    cartlist = request.session.get('cartlist',{})
    total_money = 0 
    for vo in cartlist.values():
        total_money += vo['num']*vo['price']
    request.session['total_money'] = total_money 
    

    return render(request,"Web/index.html",context)
def webindex(request):
    ''' Ordering System Homepage'''
    return render(request,"Web/index.html")
def login(request):
    '''load the login form'''
    return render(request,"web/login.html")

def dologin(request):
    ''' perform the login operation'''
    try:
        if request.POST['code'] != request.session['verifycode']:
            return redirect(reverse('web_login')+"?errinfo=2")

        #Obtain user information based on login account
        user = User.objects.get(username=request.POST['username'])
        #Check whether the current user is valid or an administrator
        if user.status == 6 or user.status == 1:
            #identify whether the password is valid
            import hashlib
            md5 = hashlib.md5()
            s = request.POST['pass']+user.password_salt #Get the password from the form and add an interference value
            md5.update(s.encode('utf-8')) 
            if user.password_hash == md5.hexdigest() :#get the value of MD5
                print('login successfully!')
                request.session['webuser'] = user.toDict()
                return redirect(reverse('web_index'))
            else:
               return redirect(reverse('web_login')+"?errinfo=5")

        else :
            return redirect(reverse('web_login')+"?errinfo=4")
    except Exception as err:
        print(err)
        return redirect(reverse('web_login')+"?errinfo=3")
  

def logout(request):
    ''' perform the logout operation'''
    del request.session['webuser']
    return redirect(reverse('web_login'))
    
def verify(request):
    ''' generate a verification code'''
     #Output verification code
    import random
    from PIL import Image, ImageDraw, ImageFont
    
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    
    im = Image.new('RGB', (width, height), bgcolor)
  
    draw = ImageDraw.Draw(im)
    
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    
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

 