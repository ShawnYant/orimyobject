#order information management
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator

from myadmin.models import Orders,OrderDetail,Payment

# Create your views here.

def index(request):
    
    umod = Orders.objects
    sid = 1 #Get the current store ID
    ulist = umod.filter(shop_id=sid)   #all order information
    mywhere=[]
    status = request.GET.get('status','')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status="+status)
        
    ulist = ulist.order_by("-id")
    

    context = {"orderslist":ulist,'mywhere':mywhere}
    # context = {"orderslist":ulist}
    return render(request,"web/list.html",context)


def insert(request):
    ''' Execute order adding '''
    try:
        
        od = Orders()
       
        od.shop_id = 1
        od.member_id = 0
        od.user_id =0
        od.name = request.GET.get('customername', '')
        od.address = request.GET.get('address','')
        od.phone_number = request.GET.get('phonenumber','')
        od.money = request.session['total_money']
        od.status = 1 #Order status :1 in processing /2 invalid /3 completed
        od.payment_status = 2 #Payment status :1 unpaid /2 paid /3 refunded
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()

        #Perform payment information addition
        op = Payment()
        op.order_id = od.id 
        op.member_id = 0
        op.type = 2
        op.bank = request.GET.get("bank",3) 
        op.money = request.session['total_money']
        op.status = 2 
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()

        #Perform the addition of order details
        cartlist = request.session.get("cartlist",{}) 
       
        for item in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id  
            ov.product_id = item['id']  
            ov.product_name = item['name'] 
            ov.price = item['price']     
            ov.quantity = item['num']  
            ov.status = 1 
            ov.save()

        del request.session["cartlist"]
        del request.session['total_money']
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")

def detail(request):
    ''' Loading Order Details '''
    oid = request.GET.get("oid",0)
    dlist = OrderDetail.objects.filter(order_id=oid)
    context = {"detaillist":dlist}
    return render(request,"web/detail.html",context)

def status(request,pid):
    ''' Modify order status '''
    try:
        
       
        umod = Orders.objects
        sid = 1 #Get the current store ID
        ulist = umod.filter(shop_id=sid)   #all object of order information
        # pid = request.GET.get("pid",0)
        if request.method == 'GET':
            ob = ulist.get(id=pid)
            print("idsuccess11"+pid)
            print(request)
            ob.status = 3

            print("status sucesssul")
            ob.save()

        print("save sucesssul")
        context = {"orderslist":ulist}    #obtain all object of order information
        print("contextend")
        
   
    except Exception as err:
         print(err)
         context = {'info':" Update Failed!！"}

    return render(request,"web/list.html",context=context) 

def status2(request,pid):

    ''' Modify order status '''
    try:
      
        umod = Orders.objects
        sid = 1 #Get the current store ID
        ulist = umod.filter(shop_id=sid)   #all object of order information
        # pid = request.GET.get("pid",0)
        if request.method == 'GET':
            ob = ulist.get(id=pid)
            print("idsuccess11"+pid)
            print(request)
            ob.status = 4

            print("status sucesssul")
            ob.save()

        print("save sucesssul")
        context = {"orderslist":ulist}    #obtain all object of order information
        print("contextend")
        
   
    except Exception as err:
         print(err)
         context = {'info':" Update Failed!！"}

    return render(request,"web/list.html",context=context)    

def status3(request):
    
    try:
        oid = request.GET.get("oid",0)
        ob = Orders.objects.get(id=oid)
        ob.status = 4
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")
