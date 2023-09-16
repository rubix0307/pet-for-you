"""
URL configuration for pet_for_you project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from user import views as user_views

urlpatterns = [
    path('', include('main.urls')),
    path('animal/', include('animal.urls')),
    path('blog/', include('blog.urls')),

    path('profile/', include('user.urls')),
    path('auth/', user_views.user_auth, name='user_auth'),
    path('logout/', user_views.user_logout, name='logout'),

    path('admin/', admin.site.urls),
]

