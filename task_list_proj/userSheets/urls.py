from django.urls import path

from . import views

urlpatterns = [
    path("<int:user_id>/get-user-sheets", views.get_user_sheets, name="get_user_sheets"),
    path("<int:user_id>/get-sheet-by-id/<str:sheet_id>", views.get_sheet_by_id, name="get_sheet_by_id"),
]

