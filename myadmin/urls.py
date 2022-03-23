#The child route of the backend management system
from django.urls import path
from myadmin.views import index
from myadmin.views import user
from myadmin.views import category
from myadmin.views import product


urlpatterns = [
    path('', index.index,name="myadmin_index"), #the home page of the back-end

    #The routes of The background administrator logs in /out
    path('login', index.login,name="myadmin_login"),#loading the login form
    path('dologin', index.dologin,name="myadmin_dologin"),#perform the login 
    path('logout', index.logout,name="myadmin_logout"),#perform the logout
    path('verify', index.verify,name="myadmin_verify"),#output the verification code



    #The routes of the employee information management
    path('user/<int:pIndex>', user.index,name="myadmin_user_index"),  #view
    path('user/add', user.add,name="myadmin_user_add"),  #add the form
    path('user/insert', user.insert,name="myadmin_user_insert"),  #perform the adding
    path('user/del/<int:uid>', user.delete,name="myadmin_user_delete"), #perform the deleting
    path('user/edit/<int:uid>', user.edit,name="myadmin_user_edit"), #loading the Edit form
    path('user/update/<int:uid>', user.update,name="myadmin_user_update"), #perform the editing

       #The routes of the category of meal information management
    path('category/<int:pIndex>', category.index,name="myadmin_category_index"),  #view
    path('category/add', category.add,name="myadmin_category_add"),  #add the form
    path('category/insert', category.insert,name="myadmin_category_insert"),  #perform the adding
    path('category/del/<int:cid>', category.delete,name="myadmin_category_delete"), #perform the deleting
    path('category/edit/<int:cid>', category.edit,name="myadmin_category_edit"), #loading the Edit form
    path('category/update/<int:cid>', category.update,name="myadmin_category_update"), #perform the editing

      #The routes of the  meal information management
    path('product/<int:pIndex>', product.index, name="myadmin_product_index"),
    path('product/add', product.add, name="myadmin_product_add"),
    path('product/insert', product.insert, name="myadmin_product_insert"),
    path('product/del/<int:pid>', product.delete, name="myadmin_product_del"),
    path('product/edit/<int:pid>', product.edit, name="myadmin_product_edit"),
    path('product/update/<int:pid>', product.update, name="myadmin_product_update"),




]
