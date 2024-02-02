from django.urls import path
from . import views


urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path("activate/<str:uidb64>/<str:token>/",views.activate,name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<str:uidb64>/<str:token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('myorders/',views.myorders,name='myorders'),
    path('order_detail/<int:order_id>/',views.order_detail,name='order_detail'),
    path('editProfile/',views.editProfile,name='editProfile'),
    path('changepassword/',views.changePassword,name='changePassword'),


]