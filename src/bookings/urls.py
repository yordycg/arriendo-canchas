from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.booking_list, name="booking_list"),
    path("nueva/", views.booking_create, name="booking_create"),
    path("ajax/get-blocks/", views.get_available_blocks,
         name="get_available_blocks"),
    path("cancelar/<str:tipo>/<int:id>/",
         views.booking_cancel, name="booking_cancel"),
    path("pagar/<str:tipo>/<int:id>/",
         views.booking_pay, name="booking_pay"),
]
