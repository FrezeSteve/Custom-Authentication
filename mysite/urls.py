"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from rest_framework import routers
from accounts import views

router = routers.DefaultRouter()
router.register(r'users', views.AccountViewSet, basename='account')

urlpatterns = [
    path('accounts/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns

"""
####### login
curl -X POST http://127.0.0.1:8000/auth/token/login/ --data 'email=djoser@gmail.com&password=testpassword'
####### protected endpoint
curl -LX GET http://127.0.0.1:8000/auth/users/me/ -H 'Authorization: Token 27f274b5252cceb0c2aff62b6aae7a63d7ae21bb' 
####### logout
curl -X POST http://127.0.0.1:8000/auth/token/logout/ -H 'Authorization: Token 27f274b5252cceb0c2aff62b6aae7a63d7ae21bb'
"""