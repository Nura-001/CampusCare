from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts import views as account_views

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),

    # Home page
    path('', account_views.home, name='home'),

    # Student registration
    path(
        'accounts/register/',
        account_views.register,
        name='register'
    ),

    # Student login
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    # Logout
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    # Student dashboard
    path(
        'dashboard/',
        account_views.dashboard,
        name='dashboard'
    ),

    # Student complaint management
    path(
        'complaints/',
        include('complaints.urls')
    ),

    # Staff dashboard and complaint management
    path(
        'staff/',
        include('adminpanel.urls')
    ),
]