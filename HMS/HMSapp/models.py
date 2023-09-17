# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminLogin(models.Model):
    username = models.CharField(db_column='Username', primary_key=True, max_length=15)  # Field name made lowercase.
    password = models.TextField(db_column='Password')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin_login'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Billing(models.Model):
    billing_id = models.AutoField(db_column='Billing_ID', primary_key=True)  # Field name made lowercase.
    user_id = models.CharField(db_column='User_ID', max_length=15, blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    history = models.IntegerField(db_column='History', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'billing'


class Booking(models.Model):
    id = models.IntegerField(primary_key=True, db_column='Booking_ID')
    room = models.ForeignKey('Room', models.DO_NOTHING, db_column='Room_ID', blank=True, null=True)
    billing = models.ForeignKey(Billing, models.DO_NOTHING, db_column='Billing_ID', blank=True, null=True)
    currentdate = models.DateField(db_column='CurrentDate', blank=True, null=True)
    numberofdays = models.IntegerField(db_column='NumberOfDays', blank=True, null=True)
    hasrated = models.TextField(db_column='HasRated', blank=True, null=True)
    isbooked = models.TextField(db_column='isBooked', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking'


class Customer(models.Model):
    cnic = models.CharField(db_column='CNIC', primary_key=True, max_length=15)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=13, blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    dob = models.DateField(db_column='DOB', blank=True, null=True)  # Field name made lowercase.
    password = models.TextField(db_column='Password')  # Field name made lowercase.
    paymenthistory = models.FloatField(db_column='PaymentHistory', blank=True, null=True)  # Field name made lowercase.
    securityquestion1 = models.ForeignKey('Securityquestions', models.DO_NOTHING, db_column='SecurityQuestion1', blank=True, null=True)  # Field name made lowercase.
    answer1 = models.TextField(db_column='Answer1', blank=True, null=True)  # Field name made lowercase.
    securityquestion2 = models.ForeignKey('Securityquestions', models.DO_NOTHING, db_column='SecurityQuestion2', related_name='customer_securityquestion2_set', blank=True, null=True)  # Field name made lowercase.
    answer2 = models.TextField(db_column='Answer2', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Hotel(models.Model):
    branch_id = models.AutoField(db_column='Branch_ID', primary_key=True)  # Field name made lowercase.
    location = models.TextField(db_column='Location', blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=13, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hotel'


class Menu(models.Model):
    food_id = models.AutoField(db_column='Food_ID', primary_key=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    cuisine = models.TextField(db_column='Cuisine', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    price = models.IntegerField(db_column='Price', blank=True, null=True)  # Field name made lowercase.
    image = models.TextField(db_column='Image', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'menu'


class Orders(models.Model):
    food_id = models.IntegerField(db_column='Food_ID', blank=True, null=True)  # Field name made lowercase.
    billing_id = models.IntegerField(db_column='Billing_ID', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orders'


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
    rating = models.FloatField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.
    noofusersrated = models.IntegerField(db_column='NoOfUsersRated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'roomtype'


class Salesandoffers(models.Model):
    offer_id = models.AutoField(db_column='Offer_ID', primary_key=True)  # Field name made lowercase.
    occasion = models.TextField(db_column='Occasion', blank=True, null=True)  # Field name made lowercase.
    percentage = models.FloatField(db_column='Percentage', blank=True, null=True)  # Field name made lowercase.
    image = models.TextField(db_column='Image', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'salesandoffers'


class Securityquestions(models.Model):
    question_id = models.AutoField(db_column='Question_ID', primary_key=True)  # Field name made lowercase.
    text = models.TextField(db_column='Text')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'securityquestions'


class Selectedoffers(models.Model):
    offer_id = models.IntegerField(db_column='Offer_ID', blank=True, null=True)  # Field name made lowercase.
    billing_id = models.IntegerField(db_column='Billing_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'selectedoffers'
