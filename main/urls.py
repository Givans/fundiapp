from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('admin_page', views.admin_page, name='admin_page'),
    path('technician', views.technician, name='technician'),
    path('customer', views.customer, name='customer'),
    path('request_repair', views.request_repair, name='request_repair'),
    path('add_staff', views.add_staff, name='add_staff'),
    path('assign_task', views.assign_task, name='assign_task'),
    path('task_completed/<str:serial>', views.task_completed, name='task_completed'),
    path('payments/<str:serial>', views.payments, name='payments'),
    path('review/<str:serial>', views.review, name='review'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
]
