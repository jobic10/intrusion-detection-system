
from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('fetch/', views.fetch, name='fetch'),
    path('block/<int:id>/', views.block, name='block'),
    path('ignore/<int:id>/', views.ignore, name='ignore'),
    path("submit/", views.submit, name='submit'),
    path("course/print", views.print_form, name='print_form'),
    path("course/registration", views.reg_form, name='reg_form'),
]
