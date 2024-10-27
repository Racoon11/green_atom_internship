from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_org", views.create_org, name="create_org"),
    path("create_storage", views.create_storage, name='create_storage'),
    path("organization/<str:name>/", views.get_org),
    path("storage/all", views.get_all_storages),
    path("storage/<str:name>/", views.get_storage),
    path("generate", views.generate),
    path("send_automatically", views.send, name='send_automatically'),
    path("closest_storage", views.closest_storage),
    path("get_queue", views.get_queue)
]
