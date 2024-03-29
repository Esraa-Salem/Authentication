"""
URL configuration for mydrfproject project.

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
# mydrfproject/urls.py

 
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
#from rest_framework.authtoken import views as authtoken_views
from django.contrib import admin
from django.urls import path, include 
schema_view = get_schema_view(
    openapi.Info(
        title="Graduation API",
        default_version="v1",
        description="Graduation API v1",
        terms_of_service="",
        #contact=openapi.Contact(email="sivaperumal2000@gmail.com"),
    ),
    public=True,
    #urlconf="accounts.urls",
)

urlpatterns = [
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="v1-schema-swagger-ui",
    ),
    path('admin/', admin.site.urls,name='admin'),
        #path('api-token-auth/',authtoken_views.obtain_auth_token),
        path('app/', include('accounts.urls')),
]
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)