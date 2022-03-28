from django.contrib import admin
from .models import Contact, Update, Technician, Customer, Category, Jobs, Task, Review

# Register your models here.
admin.site.register(Contact)
admin.site.register(Update)
admin.site.register(Technician)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Jobs)
admin.site.register(Task)
admin.site.register(Review)
