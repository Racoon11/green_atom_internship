from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_org", views.create_org, name="create_org"),
    path("create_storage", views.create_storage, name='create_storage'),
]
