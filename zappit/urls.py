"""zappit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from posts.api import viewset

urlpatterns = [
    path('admin/', admin.site.urls),
    # List All posts
    path('api/posts', viewset.PostList.as_view()),
    # List a specific post
    path('api/posts/<int:pk>', viewset.PostRetrieveDestroy.as_view()),
    # Vote API Page
    path('api/posts/<int:pk>/vote', viewset.VoteCreate.as_view()),
    # Use default login os the Rest Framework
    path('api-auth/', include('rest_framework.urls')),
]


