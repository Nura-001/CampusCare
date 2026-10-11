from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.home, name='home'),
    path('accounts/register/', account_views.register, name='register'),
    path('accounts/login/',
         auth_views.LoginView.as_view(redirect_authenticated_user=True),
         name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', account_views.dashboard, name='dashboard'),
    path('complaints/', include('complaints.urls')),
]