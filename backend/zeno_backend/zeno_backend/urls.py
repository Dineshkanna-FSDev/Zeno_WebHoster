"""
URL configuration for zeno_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from deploy.views import serve_site

urlpatterns = [
    # API endpoints (upload, etc.)
    path('api/', include('deploy.urls')),

    # make the deployed sites available without the /api/ prefix
    path('sites/<str:site_id>/', serve_site),
    path('sites/<str:site_id>/<path:path>', serve_site),
]
