from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url

urlpatterns = [
    path('accounts/', include("accounts.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                      path('admin/', admin.site.urls),

                  ] + urlpatterns

urlpatterns.append(path('', include("blog.urls")))
