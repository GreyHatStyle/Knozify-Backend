"""
URL configuration for knozify project.

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
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    # path('', lambda request: render(request, "index.html"), name="home"),
    path('', lambda request: redirect("https://knozify-web.vercel.app/"), name="home"),

    path('admin/', admin.site.urls),
    path("search/", include("watson.urls", namespace="watson")),
]

# Apps Urls
urlpatterns += [
    path('account/', include('account.urls')),
]
