from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'customers'
urlpatterns = [
    path('register/',  views.RegisterView.as_view(),           name='register'),
    path('profile/',   views.ProfileView.as_view(),            name='profile'),
    path('dashboard/', views.CustomerDashboardView.as_view(),  name='dashboard'),
 
    # Auth — use Django built-ins; swap templates as needed
    path('login/',     auth_views.LoginView.as_view(
                           template_name='customers/login.html',
                           next_page='customers:dashboard',
                       ), name='login'),
    path('logout/',    auth_views.LogoutView.as_view(
                           next_page='core:home',
                       ), name='logout'),
 
    path('password/change/', auth_views.PasswordChangeView.as_view(
                                 template_name='customers/password_change.html',
                                 success_url='/customers/password/change/done/',
                             ), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
                                      template_name='customers/password_change_done.html',
                                  ), name='password_change_done'),
]