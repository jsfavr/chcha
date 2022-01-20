"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topicshttps://github.com/jsfavr/django-ecom/settings/http/urls/
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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Django Backend API",
        default_version='v1',
        description="Multi Vendor Ecommerce API Server",
        terms_of_service="",
        contact=openapi.Contact(email="contact@f.local"),
        license=openapi.License(name="HCB Enterprise"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('category/', include('category.urls')),
    path('product/', include('product.urls')),
    path('address/', include('address.urls')),
    path('wallet/', include('wallet.urls')),
    path('cart/', include('cart.urls')),
    path('banner/', include('banner.urls')),
    path('other/', include('other.urls')),
    path('userDetails/', include('userDetails.urls')),
    path('booking/', include('booking.urls')),
    path('checkout/', include('checkout.urls')),
    path('shop/', include('shop.urls')),
    path('pos/', include('pos.urls')),
    path('service/', include('service.urls')),
    path('ads/', include('ads.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
