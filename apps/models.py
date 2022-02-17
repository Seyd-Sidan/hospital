from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class user_detls(models.Model):
    user_ids = models.IntegerField()
    phone_number = models.CharField(max_length=100, default='')


class doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    gender = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class admin_table(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class appointment(models.Model):
    date = models.DateField()
    slot_1 = models.IntegerField(default=0)
    slot_2 = models.IntegerField(default=0)
    slot_3 = models.IntegerField(default=0)
    slot_4 = models.IntegerField(default=0)
    slot_5 = models.IntegerField(default=0)
    doctor = models.ForeignKey(doctor, on_delete=models.CASCADE)
    #usr = models.ForeignKey(User, on_delete=models.CASCADE)


class booking(models.Model):
    b_date = models.CharField(max_length=100)
    slot = models.CharField(max_length=50)
    doc_name = models.CharField(max_length=50)
    b_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date

class products(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    warning = models.TextField()

class med_history(models.Model):
    u_id = models.IntegerField()
    p_name = models.CharField(max_length=100)
    p_description = models.TextField()
    p_quantity = models.IntegerField()
    p_price = models.IntegerField()


class cart(models.Model):
    p_name = models.CharField(max_length=100)
    p_qty = models.IntegerField()
    p_price = models.IntegerField()
    p_user = models.ForeignKey(User, on_delete=models.CASCADE)
