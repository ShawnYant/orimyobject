
# The view file for meal information management
from django.core import paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
import time,os
# Create your views here.
from myadmin.models import Product,Category

def index(request,pIndex=1):
    '''view information'''
    smod=Product.objects
    mywhere=[]
    list=smod.filter(status__lt=9) 
    


    #Grab and determine the search criteria
    kw=request.GET.get("keyword",None)
    if kw:
       
        list = list.filter(name__contains=kw)
        mywhere.append("keyword="+kw)

  
    cid = request.GET.get('category_id','')
    if cid != '':
        list = list.filter(category_id=cid)
        mywhere.append("category_id="+cid)


    status = request.GET.get('status','')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status="+status)


    #Perform Paging
    pIndex=int(pIndex)
    page = Paginator(list,10) # 10 Data per page
    maxpages = page.num_pages 
    #determine if the current page is out of bounds
    if pIndex > maxpages:
        pIndex=maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #grab the data of current page
    plist=page.page_range #grab the page number list

    for vo in list2:
        cob = Category.objects.get(id=vo.category_id)
        vo.categoryname = cob.name



    context = {"productlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/product/index.html",context)
    

def add(request):
    '''load the information| add the form'''
    clist = Category.objects.values("id","name")
    context = {"categorylist":clist}
    return render(request,"myadmin/product/add.html",context)

def insert(request):
    '''Execute the information adding '''
    try:
       
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return HttpResponse("There is no cover to upload file information")
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/product/"+cover_pic,"wb+")
        for chunk in myfile.chunks():    
            destination.write(chunk)  
        destination.close()


        ob=Product()
        #ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Add!！"}

    except Exception as err:
        print(err)
        context = {'info':"Addition Failed!！"}
    return render(request,"myadmin/info.html",context)

def delete(request,pid=0):
    '''Execute the information deleting'''
    try:
        ob = Product.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Successfully Delete!！"}

    except Exception as err:
        print(err)
        context = {'info':" Deletion Failed!！"}
    return render(request,"myadmin/info.html",context)

def edit(request,pid=0):
    '''load the information| edit the form'''
    try:
        ob = Product.objects.get(id=pid)
        clist = Category.objects.values("id","name")
        context = {'product':ob,"categorylist":clist}
        return render(request,"myadmin/product/edit.html",context)
    except Exception as err:
        print(err)
        context = {'info':" No information to modify was found！"}
        return render(request,"myadmin/info.html",context)

def update(request,pid=0):
    '''Execute the information modifing'''
    try:
        oldpicname = request.POST['oldpicname']

        
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            cover_pic = oldpicname
        else:
            cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
            destination = open("./static/uploads/product/"+cover_pic,"wb+")
            for chunk in myfile.chunks():     
                destination.write(chunk)  
            destination.close()



        ob = Product.objects.get(id=pid)
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info':"Updated Successfully！"}

        if myfile:
            os.remove("./static/uploads/product/"+oldpicname)


    except Exception as err:
        print(err)
        context = {'info':" Update Failed!！"}
        if myfile:
            os.remove("./static/uploads/product/"+cover_pic)

    return render(request,"myadmin/info.html",context)
    
    