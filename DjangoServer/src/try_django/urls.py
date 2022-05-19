"""try_django URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings


from targets.views import (
    get_target,
    all_targets,
    split_view
)

from .views import (
    home_page,
    contact_page,
    tower
)

urlpatterns = [
    path('', home_page),
    path('targets/', all_targets),
    path('targets/<int:target_id>', get_target),
    path('split', split_view),
    path('split/connect', split_view),
    path('split/disconnect', split_view),
    path('render/', tower),
    #path('targets/', get_target),
    path('contact/', contact_page),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
