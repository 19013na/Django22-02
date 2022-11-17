"""myDjangoPrj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ #IP주소/
    path("admin/", admin.site.urls), # IP주소/admin
    path('blog/', include('blog.urls')),    # IP주소/blog
    # blog밑에 있는 urls를 부르겠다. but, blog안에 urls가 없음. 만들자
    path('', include('single_pages.urls')),  # IP주소/
    path('accounts/', include('allauth.urls'))
]

#사진 추가
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)