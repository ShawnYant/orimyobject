#The child route of the web management system
from django.urls import path,include
from myadmin.views import registration
from web.views import index,cart
from web.views import orders
from web.views import orderhome

urlpatterns = [
    path('', index.index,name="web_index"),
    path('order', orderhome.index,name="orders_homepage"),

    #The routes of The front-end  logs in /out
    path('login', orderhome.login,name="web_orderhome_login"),#loading the login form
    path('dologin', orderhome.dologin,name="web_orderhome_dologin"),#perform the login 
    path('logout', orderhome.logout,name="web_orderhome_logout"),#perform the logout
    path('verify', orderhome.verify,name="web_orderhome_verify"),#output the verification code
   
    

    path('cart/add/<str:pid>', cart.add , name="web_cart_add"), 
    path('cart/delete/<str:pid>', cart.delete , name="web_cart_delete"), 
    path('cart/clear', cart.clear , name="web_cart_clear"), 
    path('cart/change', cart.change , name="web_cart_change"), 


    path('orders', orders.index, name="web_orders_index"), 
    path('orders/insert', orders.insert, name="web_orders_insert"), 
    path('orders/detail', orders.detail, name="web_orders_detail"), 
    path('orders/status/<str:pid>', orders.status, name="web_orders_status"), 
    path('orders/status2/<str:pid>', orders.status2, name="web_orders_status2"), 
    path('orders/status3', orders.status3, name="web_orders_status_deliever"), 

    path('doregist',registration.doregist, name="myadmin_registration_doregist"),
    path('regist',registration.regist, name="myadmin_registration_regist"),

    path("order/",include([
        path('order', orderhome.webindex,name="web_orders_homepage"),
      ]))

      
]
