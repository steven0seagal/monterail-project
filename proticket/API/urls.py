
from django.urls import path, include
from . import views
from rest_framework import routers
router = routers.DefaultRouter()

router.register(r'event', views.EventDetails)

urlpatterns = [

    path('', include(router.urls)),
    path('add_data/', views.CreateExampleData.as_view(), name = 'example'),
    path('tickets/', views.EventTicketsDetails.as_view(), name= 'avaiable_tickets'),
    path('reserve_ticket/', views.MakeReservation.as_view(), name='make_reservation'),
    path('payment/', views.Payment.as_view(), name='payment'),
    path('status/', views.ReservationStatus.as_view(), name='reservation_status'),
    path('statistics/',views.Statistics.as_view(), name='statistics')
]
