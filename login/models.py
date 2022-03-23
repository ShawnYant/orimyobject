# Create your models here.
from django.db import models
from datetime import datetime


class customer(models.Model):
    username = models.CharField(max_length=50)    #Account
    nickname = models.CharField(max_length=50)    #nickname
    password_hash = models.CharField(max_length=100)#password
    password_salt = models.CharField(max_length=50)    #password interference
    email = models.EmailField(unique=True) #email
    status = models.IntegerField(default=1)    #Status:1:Available/2:Disabled/6:System Administrator/9:Delete
    create_at = models.DateTimeField(default=datetime.now)    #creat time
    update_at = models.DateTimeField(default=datetime.now)    #update time

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,'password_salt':self.password_salt,'email':self.email,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "customer"  # change the name of the table