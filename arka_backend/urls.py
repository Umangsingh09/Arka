"""
URL configuration for arka_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from projects import views as project_views

urlpatterns = [
    path('', project_views.landing, name='landing'),
    path('admin/', admin.site.urls),
    path('request-website/', project_views.request_website, name='request-website'),
    path('dashboard/', project_views.dashboard, name='dashboard'),
    path('payment/<int:request_id>/', project_views.payment_page, name='payment'),
    path('payment/callback/', project_views.payment_callback, name='payment_callback'),
    path('payment/success/<int:request_id>/', project_views.payment_success, name='payment_success'),
    path('login/', project_views.login_view, name='login'),
    path('signup/', project_views.signup_view, name='signup'),
    path('logout/', project_views.logout_view, name='logout'),
]
