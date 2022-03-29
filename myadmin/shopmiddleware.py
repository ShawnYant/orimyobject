
from django.shortcuts import redirect
from django.urls import reverse
import re

class ShopMiddleware:
    def __init__(self, get_response):  #structure method
        self.get_response = get_response
        # One-time configuration and initialization.
        #print("ShopMiddleware")

    def __call__(self,request):
        path=request.path
        print("mycall..."+path)

    
        urllist = ['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']
        # Check whether the current request is to access the backend and path is not in the URlList
        if re.match(r"^/myadmin",path) and (path not in urllist):
            # Check whether the current user is not logged in
            if "adminuser" not in request.session:
                # The login page is executed
                return redirect(reverse('myadmin_login'))
    
  
        #Checking whether to Log in (ordering system) 
        if re.match(r"^/order",path) :
            # Check whether the current user is not logged in
            # print("enter into midlemare!")
            if "webuser" not in request.session:
                # The login page is executed
                return redirect(reverse('web_orderhome_login'))


        response = self.get_response(request)


        return response


        