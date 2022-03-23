
# The view file for dish category information management
from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
# Create your views here.
from myadmin.models import Category

def index(request,pIndex=1):
    '''view information'''
    umod=Category.objects
    ulist=umod.filter(status__lt=9)  #filter out the user whose status number is 9 
    mywhere=[]
    #Grab and determine the search criteria
    kw=request.GET.get("keyword",None)
    if kw:
        ulist=ulist.filter(name__contains=kw)  #fuzzy search
        mywhere.append('keyword='+kw)
    #Perform Paging
    pIndex=int(pIndex)
    page = Paginator(ulist,10) # 10 Data per page
    maxpages = page.num_pages 
    #determine if the current page is out of bounds
    if pIndex > maxpages:
        pIndex=maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #grab the data of current page
    plist=page.page_range #grab the page number list
    context = {"categorylist":list2,"plist":plist,"pIndex":pIndex,"maxpages":maxpages,"mywhere":mywhere}
    return render(request,"myadmin/category/index.html",context)
    

def add(request):
    '''load the information| add the form'''
    return render(request,"myadmin/category/add.html")

def insert(request):
    '''Execute the information adding '''
    try:
        ob=Category()
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Add!！"}

    except Exception as err:
        print(err)
        context = {'info':"Addition Failed!！"}
    return render(request,"myadmin/info.html",context)

def delete(request,cid=0):
    '''Execute the information deleting'''
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Delete!！"}

    except Exception as err:
        print(err)
        context = {'info':" Deletion Failed!！"}
    return render(request,"myadmin/info.html",context)

def edit(request,cid=0):
    '''load the information| edit the form'''
    try:
        ob = Category.objects.get(id=cid)
        context = {'category':ob}
        return render(request,"myadmin/category/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':" No information to modify was found！"}
        return render(request,"myadmin/info.html",context)

def update(request,cid=0):
    '''Execute the information modifing'''
    try:
        ob = Category.objects.get(id=cid)
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Updated Successfully！"}
    except Exception as err:
        print(err)
        context = {'info':" Update Failed!！"}
    return render(request,"myadmin/info.html",context)