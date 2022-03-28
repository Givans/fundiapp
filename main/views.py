import random

from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Contact, Jobs, Technician, Task, Customer, Review
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.user.is_superuser and request.user.is_staff:
        return redirect(admin_page)
    elif request.user.is_staff:
        return redirect(technician)
    else:
        return redirect(customer)


@login_required(login_url='login')
def customer(request):
    if not request.user.is_staff and not request.user.is_superuser and request.user.is_authenticated:
        username = request.user.username
        uploads = Jobs.objects.filter(name=username).order_by('id').reverse()
        all_uploads = Jobs.objects.filter(name=username).count()

        context = {
            'uploads': uploads,
            'all_uploads': all_uploads,
        }
        return render(request, 'customer/index.html', context)
    else:
        return redirect(home)


@login_required(login_url='login')
def technician(request):
    if request.user.is_staff and not request.user.is_superuser:
        username = request.user.username
        tasks = Task.objects.filter(tech=username, status='accepted').order_by('id').reverse()
        records = Jobs.objects.filter(status='completed').order_by('id').reverse()
        tasks_no = Task.objects.filter(tech=username).count()

        context = {
            'tasks': tasks,
            'task_no': tasks_no,
        }
        return render(request, 'technician/index.html', context)
    else:
        return redirect(home)


@login_required(login_url='login')
def admin_page(request):
    if request.user.is_superuser:
        uploads = Jobs.objects.all().order_by('id').reverse()
        records = Jobs.objects.filter(status='completed').order_by('id').reverse()
        members = User.objects.all().order_by('id').reverse()
        all_uploads = Jobs.objects.all().count()
        technicians = Technician.objects.all().order_by('id').reverse()
        all_records = Jobs.objects.filter(status='completed').count()
        all_users = User.objects.all().count()

        user_status = 'unknown'
        for m in members:
            if m.is_superuser:
                user_status = 'Administrator'
            elif m.is_staff:
                user_status = 'Technician'
            else:
                user_status = 'Customer'

        context = {
            'requests': uploads,
            'all_uploads': all_uploads,
            'technicians': technicians,
            'records': records,
            'all_records': all_records,
            'members': members,
            'all_users': all_users,
            'user_status': user_status,
        }
        return render(request, 'admin_page/index.html', context)
    else:
        return redirect(home)


@login_required(login_url='login')
def request_repair(request):
    if request.user.is_authenticated and not request.user.is_staff:
        if request.method == 'POST':
            description = request.POST['description']
            location = request.POST['location']
            photo = request.FILES['photo']

            username = request.user.username

            def random_no():
                a = random.random()
                b = a * 1000000000
                c = int(b)
                product_serial = 'Job' + str(c)
                check = Jobs.objects.filter(serial=product_serial).exists()
                if check:
                    return random_no()
                else:
                    return product_serial

            serial = random_no()

            instance = Jobs.objects.create(description=description, status='pending', location=location, pic=photo,
                                           name=username, serial=serial)
            instance.save()
            messages.success(request, 'job uploaded successfully, wait for the feedback')
            return redirect(customer)
        else:
            return redirect(customer)
    else:
        messages.error("unauthorized access")
        return redirect('/')


@login_required(login_url='login')
def add_staff(request):
    if request.user.is_superuser and request.user.is_staff:
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            idno = request.POST['idno']
            email = request.POST['email']
            age = request.POST['age']
            address = request.POST['address']
            username = request.POST['username']
            password = request.POST['password']
            password2 = request.POST['password2']

            if int(age) >= 18:

                if password == password2:
                    if User.objects.filter(email=email).exists():
                        messages.info(request, 'Email already in use')
                        return redirect(admin_page)
                    elif User.objects.filter(username=username).exists():
                        messages.info(request, 'Username already in use')
                        return redirect(admin_page)
                    else:
                        user = User.objects.create_user(first_name=firstname, last_name=lastname, is_staff=True,
                                                        username=username, email=email, password=password)

                        member = User.objects.get(username=username)
                        staff = Technician.objects.create(member=member, first_name=firstname, last_name=lastname,
                                                          username=username, email=email, idno=idno, age=age,
                                                          address=address)
                        staff.save()
                        user.save()

                        messages.info(request, 'staff added successfully')
                        return redirect(admin_page)
                else:
                    messages.error(request, 'password mismatch')
                    return redirect(admin_page)
        else:
            messages.warning(request, 'age restricted')
            return redirect(admin_page)
    else:
        messages.error(request, "unauthorized access")
        return redirect('/')


@login_required(login_url='login')
def assign_task(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            description = request.POST['description']
            image = request.POST['image']
            location = request.POST['location']
            tech = request.POST['technician']

            try:
                job = Jobs.objects.get(description=description)
                if job.location == location:
                    job.status = 'accepted'
                    job.class_name = 'info'
                    job.status_type = 'button'
                    job.save()
                else:
                    job.status = 'pending'
                    job.save()
                    messages.error(request, 'unknown error')
                    return redirect(admin_page)
            except:
                messages.error(request, "unknown error. Try again")
                return redirect(admin_page)

            def random_no():
                a = random.random()
                b = a * 1000000000
                c = int(b)
                product_serial = 'Task' + str(c)
                check = Task.objects.filter(serial=product_serial).exists()
                if check:
                    return random_no()
                else:
                    return product_serial

            serial = random_no()

            instance = Task.objects.create(description=description, status='accepted', serial=serial, image=image,
                                           location=location, tech=tech)
            instance.save()

            messages.info(request, 'Task assigned successfully')
            return redirect(admin_page)
        else:
            return redirect(admin_page)
    else:
        messages.error(request, "Unauthorized access")
        return redirect(home)


@login_required(login_url='login')
def task_completed(request, serial):
    if not request.user.is_superuser and request.user.is_staff:
        if request.method == 'POST':
            description = request.POST['description']
            location = request.POST['location']
            username = request.user.username
            instance = Task.objects.get(serial=serial)
            instance.status = 'completed'
            instance.save()
            instance2 = Jobs.objects.get(description=description, location=location)
            instance2.status = 'payments'
            instance2.user_button = 'submit'
            instance2.class_name = 'danger'
            instance2.save()

            messages.info(request, 'congratulations ' + username)
            return redirect(technician)
        else:
            return redirect(technician)
    else:
        messages.error(request, "unauthorized access")
        return redirect('/')


@login_required(login_url='login')
def payments(request, serial):
    if not request.user.is_superuser and not request.user.is_staff and request.user.is_authenticated:
        if request.method == 'POST':
            description = request.POST['description']
            location = request.POST['location']
            instance2 = Jobs.objects.get(description=description, location=location, serial=serial)
            instance2.paid = True
            instance2.status = 'Completed'
            instance2.user_button = 'button'
            instance2.class_name = 'success'
            instance2.save()

            messages.info(request, 'paid successfully')
            return redirect('https://stkot.herokuapp.com/')
        else:
            return redirect(customer)
    else:
        messages.error(request, "unauthorized access")
        return redirect('/')


def signup(request):
    if request.user.is_authenticated:
        messages.error(request, "unauthorized access")
        return redirect(home)
    else:
        if request.method == 'POST':
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            location = request.POST['location']
            phone = request.POST['phone']
            gender = request.POST['gender']
            pic = request.FILES['pic']
            password = request.POST['password']
            password2 = request.POST['password2']

            if username == 'admin' or 'Admin':

                if password == password2:
                    if User.objects.filter(email=email).exists():
                        messages.info(request, 'Email error')
                        return redirect('/')
                    elif User.objects.filter(username=username).exists():
                        messages.info(request, 'Username error')
                        return redirect('/')
                    elif Customer.objects.filter(phone=phone).exists():
                        messages.info(request, 'Phone number error')
                        return redirect('/')
                    else:
                        user = User.objects.create_user(first_name=firstname, last_name=lastname, is_staff=False,
                                                        is_superuser=False, username=username, email=email,
                                                        password=password)

                        user.save()
                        member = User.objects.get(username=username)
                        instance = Customer.objects.create(member=member, first_name=firstname, last_name=lastname,
                                                           username=username, email=email, phone=phone, profile=pic,
                                                           address=location, gender=gender)
                        instance.save()

                        messages.info(request, 'Account created successfully!! Now login')
                        return redirect('/')
                else:
                    messages.error(request, 'password mismatch')
                    return redirect('/')
        else:
            messages.warning(request, 'username restricted')
            return redirect('/')


@login_required(login_url='login')
def contact(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            subject = request.POST['subject']
            message = request.POST['message']

            try:
                instance = Contact.objects.create(name=name, email=email, subject=subject, message=message)
                instance.save()
                messages.success(request, 'message sent successfully')
                return redirect(customer)
            except:
                messages.error(request, 'unknown error. Try again')
                return redirect(customer)
        else:
            return redirect(customer)
    else:
        messages.warning(request, 'kindly login')
        return redirect('/')


@login_required(login_url='login')
def review(request, serial):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']
            message = request.POST['message']

            try:
                instance = Review.objects.create(name=name, serial=serial, message=message)
                instance.save()
                messages.success(request, 'Review sent successfully')
                return redirect(customer)
            except:
                messages.error(request, 'unknown error. Try again')
                return redirect(customer)
        else:
            return redirect(customer)
    else:
        messages.warning(request, 'kindly login')
        return redirect('/')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Success!! logout..')
    return redirect('/')
