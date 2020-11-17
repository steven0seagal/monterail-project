import datetime
import random
import string
from collections import Counter

import pytz
from django.http import Http404
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Ticket
from .serializers import EventSerializer
from .utils import CardError, CurrencyError, PaymentError, PaymentGateway


def get_object_event(pk):
    "Get object from Event database by its pk"
    try:
        return Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404


def get_object_ticket(pk):
    "Get object from Ticket database by its pk"
    try:
        return Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        raise Http404


def dummy_token_creator(*args):
    "Create random string"
    return ''.join(random.choices(string.ascii_uppercase
                   + string.digits, k=25))


class CreateExampleData(APIView):

    """
    Class that will populate our database one time only
    """

    def get(self, request, format=None):

        # 1st event
        example_date = datetime.datetime(
            2018, 7, 29, 12, 0, 13, tzinfo=pytz.UTC)
        new_event = Event(name='Test event1', date=example_date)
        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='REGULAR',
                                    price=55.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='BUDGET',
                                   price=45.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='PREMIUM',
                                    price=95.00)
            ticket_premium.save()
            ticket_VIP = Ticket(event=new_event, type='VIP',
                                price=155.00)
            ticket_VIP.save()
        new_event = Event(name='Test event2', date=example_date)
        new_event.save()

        # 2nd event
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='REGULAR',
                                    price=45.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='BUDGET',
                                   price=30.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='PREMIUM',
                                    price=100.00)
            ticket_premium.save()
            ticket_VIP = Ticket(event=new_event, type='VIP',
                                price=155.00)
            ticket_VIP.save()

        # 3rd event
        new_event = Event(name='Test event3', date=example_date)
        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='REGULAR',
                                    price=55.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='BUDGET',
                                   price=50.00)
            ticket_budget.save()

        return Response(status=status.HTTP_201_CREATED)


class EventDetails(viewsets.ModelViewSet):

    """
    Class that contain function to correctly view
    what kind of events are avaiable
    """

    http_method_names = ['get', 'post', 'head', 'options']
    queryset = Event.objects.all().order_by('name')
    serializer_class = EventSerializer


class EventTicketsDetails(APIView):

    """
    Clas that contain function to get data about tickets
    """

    def get(self, request, format=None):
        '''Get data about avaiable tickets'''

        if 'id' in request.data:

            found_event = get_object_event(request.data['id'])

            all_tickets = Ticket.objects.filter(event=found_event)
            all_types = all_tickets.values_list('type', flat=True)
            avaiable_tickets = {}
            for i in all_types:
                avaiable_tickets[i] = 0

            for ticket in all_tickets:
                if ticket.reserved_until < timezone.now() and ticket.sold_status is False:
                    avaiable_tickets[ticket.type] += 1

            return Response(avaiable_tickets, status=status.HTTP_200_OK)
        else:

            return Response(status=status.HTTP_400_BAD_REQUEST)


class MakeReservation(APIView):

    """
    Class for making reservation
    """

    def put(self, request, ticket_type, event_id, format=None):
        '''Make reservation based on event id and ticket type '''
        event = get_object_event(event_id)
        tickets = Ticket.objects.filter(event=event, type=ticket_type)

        for ticket in tickets:
            if ticket.reserved_until < timezone.now() \
                and ticket.sold_status is False:
                ticket.reserved = True
                ticket.reserved_until = timezone.now() \
                    + datetime.timedelta(minutes=15)
                ticket.save()

                return_data = {
                    'ticket_id': ticket.id,
                    'event': ticket.event.name,
                    'type': ticket.type,
                    'price': str(ticket.price) + ' EUR',
                    'reserved_until': ticket.reserved_until,
                    }

                return Response(return_data,
                                status=status.HTTP_202_ACCEPTED)
        message = \
            {'message': 'There are no more tickets in that category'}
        return Response(data=message,
                        status=status.HTTP_417_EXPECTATION_FAILED)


class Payment(APIView):

    """
    Class to pay for reservation
    """

    def put(self, request):
        '''Pay for ticket based on its number'''
        if 'ticket_id' in request.data:
            ticket = get_object_ticket(request.data['ticket_id'])
            if ticket.reserved_until > timezone.now() and ticket.sold_status is False:

                # replace with payment registration via przelewy24
                token = dummy_token_creator()
                currency = 'EUR'
                try:
                    PaymentGateway.charge(self, ticket.price, token, currency)
                    ticket.sold_status = True
                    ticket.reservation_number = token
                    ticket.save()
                    return_data = {'reservation_number': token}
                    return Response(data=return_data,
                                    status=status.HTTP_200_OK)
                except CardError:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                except CurrencyError:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                except PaymentError:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ReservationStatus(APIView):

    """
    Class to check reservation number
    """

    def get_object_or_404(self, reservation_number):
        '''Get information about ticket '''
        try:
            return Ticket.objects.get(reservation_number=reservation_number)
        except Ticket.DoesNotExist:
            raise Http404

    def get(self, request):

        ticket = \
            self.get_object_or_404(reservation_number=request.data['reservation_number'])
        return_data = {
            'event_name': ticket.event.name,
            'event_date': ticket.event.date,
            'type': ticket.type,
            'price': ticket.price,
            'reservation_number': ticket.reservation_number,
            }

        return Response(return_data, status=status.HTTP_200_OK)


class Statistics(APIView):

    """
    Class to get statistics about sold tickets
    """

    def get(self, request):

        results = {}

        results['reserved_tickets_by_event_and_type'] = {}
        results['reserved_tickets_by_event'] = {}
        results['reserved_tickets_by_type'] = {}
        results['profit_by_event'] = {}
        results['event_popularity_ranking'] = {}

        events_all = Event.objects.order_by('-date')
        reserved_ticket_all = Ticket.objects.filter(sold_status=True)

        type_ticket = []
        for reserved_ticket in reserved_ticket_all:
            if reserved_ticket.sold_status is True:
                type_ticket.append(reserved_ticket.type)
        results['reserved_tickets_by_type'] = Counter(type_ticket)

        for event in events_all:
            overal_profit = 0
            results['reserved_tickets_by_event_and_type'][event.name] = \
                {}
            tickets = Ticket.objects.filter(event=event)

            if len(tickets) > 0:
                sold_tickets = []
                for ticket in tickets:
                    if ticket.sold_status is True:
                        sold_tickets.append(ticket.type)
                        overal_profit += ticket.price

                results['profit_by_event'][event.name] = overal_profit
                results['reserved_tickets_by_event_and_type'
                        ][event.name] = Counter(sold_tickets)
                results['reserved_tickets_by_event'][event.name] = \
                    len(sold_tickets)
                results['event_popularity_ranking'][event.name] = \
                    len(sold_tickets) / len(tickets)

        return Response(results, status=status.HTTP_200_OK)




      

         
        
