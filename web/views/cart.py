#ordering list management
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from myadmin.models import User

# Create your views here.


def add(request,pid):
    ''' Add meal on the odering list '''
    product = request.session['productlist'][pid]
    product['num'] = 1 
    cartlist = request.session.get('cartlist',{})
    if pid in cartlist:
        cartlist[pid]['num'] += product['num'] 
    else:
        cartlist[pid] = product 
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))

def delete(request,pid):
    cartlist = request.session.get('cartlist',{})
    del cartlist[pid]
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))
    
def clear(request):
    ''' empty the shopping list '''
    request.session['cartlist'] = {}
    return redirect(reverse('web_index'))

def change(request):
    ''' change the information of meal on the odering list '''
   
    cartlist = request.session.get('cartlist',{})
    pid = request.GET.get("pid",0) 
    m = int(request.GET.get('num',1))
    if m < 1:
        m = 1
    cartlist[pid]['num'] = m 
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))