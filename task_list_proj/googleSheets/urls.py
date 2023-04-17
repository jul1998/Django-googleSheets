from django.urls import path
from . import views

urlpatterns = [
    path("edit/", views.calculate_sheet, name="edit"),
    path("create/", views.create_sheet, name="create"),
    path("read/", views.get_values, name="read"),
    path("batch_read/", views.batch_get_values, name="batch_read"),
    path("write/", views.update_values, name="write"),
    path("batch_write/", views.batch_update_values, name="batch_write"),
]