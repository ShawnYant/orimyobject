# import email
from django.db import models
from datetime import datetime

# Create  models here.
class cus(models.Model):
    username = models.CharField(max_length=50)    #Account
    nickname = models.CharField(max_length=50)    #nickname
    password_hash = models.CharField(max_length=100)#password
    password_salt = models.CharField(max_length=50)    #password interference
    status = models.IntegerField(default=1)    #Status:1:Available/2:Disabled/6:System Administrator/9:Delete
    create_at = models.DateTimeField(default=datetime.now)    #creat time
    update_at = models.DateTimeField(default=datetime.now)    #update time
    # email = models.EmailField(unique= True) # EMAIL
    address = models.CharField(max_length=100)   #customer address
    phoneNo = models.CharField(max_length=10)  #customer phone number
    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S'),'email':self.email,'address':self.address,'phoneNo':self.phoneNo}

    class Meta:
        db_table = "customer"  # change the name of the table