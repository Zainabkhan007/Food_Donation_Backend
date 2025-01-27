from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.register,name='register'),
    path('login/', views.login,name='login'),
    path('admin_login/', views.admin_login,name='admin_login'),
    path('contact/', views.contactus,name='contactus'),
    path('get_all_msgs/', views.get_all_msgs,name='get_all_msgs'),
    path('payment/', views.CreatePaymentIntentView.as_view(), name='create_payment_intent'),

]
