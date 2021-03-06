from account import views
from django.urls import path, include
from ecommerce_app import urls as ecommerce_app_urls
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

#########################################################################################################################################

urlpatterns = [
    
    path("signup/",views.register,name="signup"),
	path("login/",views.user_login,name="login"),
	path("check-user/",views.check_user,name="check-user"),
	path("logout/",views.user_logout,name="logout"),
	path("change-password/",views.change_password,name="change-password"),
	

#########################################################################################################################################

   	
   	path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/commons/password-reset/password_reset.html',
             subject_template_name='account/commons/password-reset/password_reset_subject.txt',
             email_template_name='account/commons/password-reset/password_reset_email.html',
             success_url='/account/user_login'
         ),
         name='password_reset'),
    

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/commons/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/commons/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/commons/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]


#########################################################################################################################################