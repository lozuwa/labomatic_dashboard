from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
  # Main
  path("", views.index, name="index"),
  path("<int:id>", views.index, name="index"),
  path("refresh", views.refresh, name="refresh") 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
