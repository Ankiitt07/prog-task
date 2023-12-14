"""prog_tech_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from app.views import signup, login, logout, add_user, authentication, images_upload, upload_image, uploaded_images, gallery

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signup, name="user_signup"),
    path('login/', login, name="user_login"),
    path('logout', logout, name="user_logout"),
    path('signup/', signup, name="user_signup"),
    path('add_user/', add_user, name="add_user"),
    path('authentication/', authentication, name="authentication"),
    path('images_upload/', images_upload, name="images_upload"),
    path('upload/', upload_image, name='upload_image'),
    path('gallery/', gallery, name='gallery')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)