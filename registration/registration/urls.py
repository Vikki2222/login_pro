"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app1 import views
from app1.views import toggle_access_rule
from app1.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/',views.SignupPage,name='signup'),
    path('',views.login,name='login'),
    path('postsign/',views.postsign,name='postsign'),
    path('logout/',views.LogoutPage,name='logout'),
    path('toggle_access_rule/', toggle_access_rule, name='toggle_access_rule'),
     path('home/',views.home,name='home'),
     path('login/', LoginView.as_view(), name='login'),
     path('api/', include('myapp.urls')),

]
