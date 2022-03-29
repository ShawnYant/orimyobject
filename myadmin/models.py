from django.db import models
from datetime import datetime


class User(models.Model):
    username = models.CharField(max_length=50)    #Account
    nickname = models.CharField(max_length=50)    #nickname
    password_hash = models.CharField(max_length=100)#password
    password_salt = models.CharField(max_length=50)    #password interference
    status = models.IntegerField(default=1)    #Status:1:Available/2:Disabled/6:System Administrator/9:Delete
    create_at = models.DateTimeField(default=datetime.now)    #creat time
    update_at = models.DateTimeField(default=datetime.now)    #update time
    email = models.EmailField(unique= True) # EMAIL
    address = models.CharField(max_length=100)   #customer address
    phoneNo = models.CharField(max_length=10)  #customer phone number
    
    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S'),'email':self.email,'address':self.address,'phoneNo':self.phoneNo}
    class Meta:
        db_table = "user"  # change the name of the table

#Dishes classification information model
class Category(models.Model):
    shop_id = models.IntegerField()       
    name = models.CharField(max_length=50)    #catogoryid
    status = models.IntegerField(default=1)        #Status :1 Valid /2 discontinued /9 deleted
    create_at = models.DateTimeField(default=datetime.now)    #Adding time
    update_at = models.DateTimeField(default=datetime.now)    #Update time

    class Meta:
        db_table = "category"  # change the name of the table

#Dish information model
class Product(models.Model):
    shop_id = models.IntegerField()       
    category_id = models.IntegerField()    #catogoryid
    cover_pic = models.CharField(max_length=50)    #picture
    name = models.CharField(max_length=50)#DishName
    price = models.FloatField()    #Price
    status = models.IntegerField(default=1)        #Status :1 Valid /2 discontinued /9 deleted
    create_at = models.DateTimeField(default=datetime.now)    #Adding time
    update_at = models.DateTimeField(default=datetime.now)    #Update time

    def toDict(self):
        return {'id':self.id,'shop_id':self.shop_id,'category_id':self.category_id,'cover_pic':self.cover_pic,'name':self.name,'price':self.price,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "product"  # change the name of the table

class Orders(models.Model):
    shop_id = models.IntegerField()   #store id
    member_id = models.IntegerField() #member id
    user_id = models.IntegerField()   #operator id
    name = models.CharField(max_length=30)    #customer name
    address = models.CharField(max_length=100)   #customer address
    phone_number = models.CharField(max_length=10)  #customer phone number
    money = models.FloatField()     #amount
    status = models.IntegerField(default=1)   #Order status 
    payment_status = models.IntegerField(default=1)   #Payment status :1 unpaid /2 paid /3 refunded
    create_at = models.DateTimeField(default=datetime.now)  #creation time
    update_at = models.DateTimeField(default=datetime.now)  #modification time

    class Meta:
        db_table = "orders"  # change the name of the table



class OrderDetail(models.Model):
    order_id = models.IntegerField()  #OrderID
    product_id = models.IntegerField()  #Food id  
    product_name = models.CharField(max_length=50) #The name of the dishes
    price = models.FloatField()     #price
    quantity = models.IntegerField()  #capacity
    status = models.IntegerField(default=1) #Status :1 Normal /9 Deleted

    class Meta:
        db_table = "order_detail"  # change the name of the table


#the following part havn't done

class Payment(models.Model):
    order_id = models.IntegerField()  #id
    member_id = models.IntegerField() #id
    money = models.FloatField()     #payment amount
    type = models.IntegerField()      #Payment method: 1 member payment /2 cashier collection
    bank = models.IntegerField(default=1) #Receiving from : debet credit paypal
    status = models.IntegerField(default=1) #Receiving bank channels :1 wechat /2 balance /3 cash /4 Alipay
    create_at = models.DateTimeField(default=datetime.now)  #creation time 
    update_at = models.DateTimeField(default=datetime.now)  #modification time

    class Meta:
        db_table = "payment"  # change the name of the table