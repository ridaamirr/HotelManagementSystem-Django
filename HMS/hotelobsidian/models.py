# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class AdminLogin(models.Model):
    username = models.CharField(db_column='Username', primary_key=True, max_length=15)  # Field name made lowercase.
    password = models.TextField(db_column='Password')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin_login'


class Billing(models.Model):
    billing_id = models.AutoField(db_column='Billing_ID', primary_key=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'billing'


class Booking(models.Model):
    room = models.ForeignKey('Room', models.DO_NOTHING, db_column='Room_ID', blank=True, null=True)  # Field name made lowercase.
    billing = models.ForeignKey(Billing, models.DO_NOTHING, db_column='Billing_ID', blank=True, null=True)  # Field name made lowercase.
    currentdate = models.DateField(db_column='CurrentDate', blank=True, null=True)  # Field name made lowercase.
    numberofdays = models.IntegerField(db_column='NumberOfDays', blank=True, null=True)  # Field name made lowercase.
    isbooked = models.TextField(db_column='isBooked', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'booking'

class Customer(models.Model):
    cnic = models.CharField(db_column='CNIC', unique=True, primary_key=True, max_length=15)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=13, blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    password = models.TextField(db_column='Password')  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'customer'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Hotel(models.Model):
    branch_id = models.AutoField(db_column='Branch_ID', primary_key=True)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=13, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hotel'


class Room(models.Model):
    room_id = models.AutoField(db_column='Room_ID', primary_key=True)  # Field name made lowercase.
    roomtype = models.ForeignKey('Roomtype', models.DO_NOTHING, db_column='RoomType_ID')  # Field name made lowercase.
    roomnumber = models.IntegerField(db_column='RoomNumber')  # Field name made lowercase.
    branch = models.ForeignKey(Hotel, models.DO_NOTHING, db_column='Branch_ID')  # Field name made lowercase.
    isbooked = models.CharField(db_column='isBooked', max_length=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'room'


class Roomtype(models.Model):
    roomtype_id = models.AutoField(db_column='RoomType_ID', primary_key=True)  # Field name made lowercase.
    numberofbeds = models.IntegerField(db_column='NumberOfBeds', blank=True, null=True)  # Field name made lowercase.
    type = models.TextField(db_column='Type', blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    image = models.TextField(db_column='Image', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roomtype'