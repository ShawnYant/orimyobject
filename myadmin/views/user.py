
# The view file for employee information management
from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
# Create your views here.
from myadmin.models import User

def index(request,pIndex=1):
    '''view information'''
    umod=User.objects
    ulist=umod.filter(status__lt=9)  #filter out the user whose status number is 9 
    mywhere=[]
    #Grab and determine the search criteria
    kw=request.GET.get("keyword",None)
    if kw:
        ulist=ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))  #fuzzy search
        mywhere.append('keyword='+kw)
    #Perform Paging
    pIndex=int(pIndex)
    page = Paginator(ulist,5) # 5 Data per page
    maxpages = page.num_pages 
    #determine if the current page is out of bounds
    if pIndex > maxpages:
        pIndex=maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #grab the data of current page
    plist=page.page_range #grab the page number list
    context = {"userlist":list2,"plist":plist,"pIndex":pIndex,"maxpages":maxpages,"mywhere":mywhere}
    return render(request,"myadmin/user/index.html",context)
    

def add(request):
    '''load the information| add the form'''
    return render(request,"myadmin/user/add.html")

def insert(request):
    '''Execute the information adding '''
    try:
        ob=User()
        ob.username = request.POST['username']
        ob.nickname = request.POST['nickname']

        #the password of the emplyee is processed by MD5
        import hashlib,random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password']+str(n) #Get the password from the form and add an interference value
        md5.update(s.encode('utf-8')) 
        ob.password_hash = md5.hexdigest() #get the value of MD5
        ob.password_salt = n

        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Add!！"}

    except Exception as err:
        print(err)
        context = {'info':"Addition Failed!！"}
    return render(request,"myadmin/info.html",context)

def delete(request,uid=0):
    '''Execute the information deleting'''
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Delete!！"}

    except Exception as err:
        print(err)
        context = {'info':" Deletion Failed!！"}
    return render(request,"myadmin/info.html",context)

def edit(request,uid=0):
    '''load the information| edit the form'''
    try:
        ob = User.objects.get(id=uid)
        context = {'user':ob}
        return render(request,"myadmin/user/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':" No information to modify was found！"}
        return render(request,"myadmin/info.html",context)

def update(request,uid=0):
    '''Execute the information modifing'''
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Updated Successfully！"}
    except Exception as err:
        print(err)
        context = {'info':" Update Failed!！"}
    return render(request,"myadmin/info.html",context)
    