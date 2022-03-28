from django.contrib.auth.models import User
from django.db import models
import datetime
from cloudinary.models import CloudinaryField


class Contact(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(max_length=2000, null=False, blank=False)
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "name: " + self.name, " => subject: " + self.subject


class Update(models.Model):
    to = models.CharField(max_length=2000)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=2000, null=False, blank=False)
    date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return "name: " + self.to


class Technician(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=12)
    email = models.EmailField()
    idno = models.IntegerField()
    age = models.IntegerField(default=18)
    date = models.DateTimeField(default=datetime.datetime.now)
    profile = CloudinaryField('fundi/images/technician')
    # profile = models.ImageField(upload_to="images", null=False, default='default.jpg')
    address = models.CharField(max_length=50, default='kitui')
    phone = models.CharField(max_length=10)
    other2 = models.CharField(max_length=50, default='Jane')
    other3 = models.CharField(max_length=50, default='phil')

    def __str__(self):
        return "name: " + self.username


class Customer(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=12)
    gender = models.CharField(max_length=12)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    date = models.DateTimeField(default=datetime.datetime.now)
    profile = CloudinaryField('fundi/images/customer')
    # profile = models.ImageField(upload_to="images", null=False, default='default.jpg')
    address = models.CharField(max_length=50, default='John')
    other1 = models.CharField(max_length=50, default='Doe')
    other2 = models.CharField(max_length=50, default='Jane')
    other3 = models.CharField(max_length=50, default='phil')

    def __str__(self):
        return "name: " + self.username


class Category(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=1)
    date = models.DateTimeField(default=datetime.datetime.now)
    other1 = models.CharField(max_length=50, default='Doe')
    other2 = models.CharField(max_length=50, default='Jane')
    other3 = models.CharField(max_length=50, default='phil')

    def __str__(self):
        return "Category: " + self.name


class Jobs(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=1)
    status_type = models.CharField(max_length=50, default='submit')
    class_name = models.CharField(max_length=50, default='danger')
    user_button = models.CharField(max_length=50, default='button')
    # satisfied = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default='pending')
    paid = models.BooleanField(default=False)
    description = models.TextField()
    location = models.CharField(max_length=100)
    pic = CloudinaryField('fundi/images/jobs')
    # pic = models.ImageField(upload_to="jobs", null=False, default='default.jpg')
    date = models.DateTimeField(default=datetime.datetime.now)
    technician = models.CharField(max_length=50, default='None')
    serial = models.CharField(max_length=50, default='Serial1234')
    other2 = models.CharField(max_length=50, default='Jane')
    other3 = models.CharField(max_length=50, default='phil')

    def __str__(self):
        return "Category: " + self.name


class Task(models.Model):
    description = models.TextField()
    image = models.CharField(max_length=250)
    location = models.CharField(max_length=250, default='Doe')
    tech = models.CharField(max_length=50, default='Jane')
    status = models.CharField(max_length=50, default='accepted')
    serial = models.CharField(max_length=50, default='Serial1234')


class Review(models.Model):
    name = models.CharField(max_length=250)
    serial = models.CharField(max_length=250)
    message = models.TextField()
