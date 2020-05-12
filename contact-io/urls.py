"""contacts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from app import urls
from users import urls as users_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urls.urlpatterns)),
    path('account/', include(users_urls.urlpatterns)),
    path('accounts/', include('allauth.urls')),
    path('', include('django.contrib.auth.urls'))  # for authentication
]

# customizing admin header -- formerly : Django administration , Site administration
admin.site.site_header = 'Contacts 4 all'
admin.site.index_title = 'Contacts Panel'
admin.site.site_title = 'kolaclan'

if settings.DEBUG:
    # Set the directory to look for media files only when in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
