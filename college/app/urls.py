from django.urls import path
from .import views

urlpatterns = [
    path('',views.landingpage,name='landingpage'),
    path('signupteachers',views.signupteachers,name='signupteachers'),
    path('adminaddcrs',views.adminaddcrs,name='adminaddcrs'),
    path('adminaddstd',views.adminaddstd,name='adminaddstd'),
    path('stddetails',views.stddetails,name='stddetails'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('loginfnc',views.loginfnc,name='loginfnc'),
    path('add_course',views.add_course,name='add_course'),
    path('addstd_details',views.addstd_details,name='addstd_details'),
    path('teacherhome',views.teacherhome,name='teacherhome'),
    path('user_sign',views.user_sign,name='user_sign'),
    path('teacherlogin',views.teacherlogin,name='teacherlogin'),
    path('teachercard',views.teachercard,name='teachercard'),
    path('tchr_edit/<int:id>',views.tchr_edit,name='tchr_edit'),
    path('teacheredit',views.teacheredit,name='teacheredit'),
    path('delete/<int:pk>',views.delete,name='delete'),
    path('stdedit/<int:pk>',views.stdedit,name='stdedit'),
    path('editdetails/<int:pk>',views.editdetails,name='editdetails'),
    path('teacherdetails',views.teacherdetails,name='teacherdetails'),
    path('tdelete/<int:pk>',views.tdelete,name='tdelete'),
    path('logout',views.logout,name='logout'),

   
    
    
]