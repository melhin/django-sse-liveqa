"""
URL configuration for sse_liveqa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

from sse_liveqa.views import health

urlpatterns = [
    path("health/", health, name="health"),
    path("qa/", include("qa.urls")),
    path("streams/", include("streams.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
