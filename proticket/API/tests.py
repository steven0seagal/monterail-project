#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections
import datetime
import json

import pytz
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Event, Ticket
from collections import Counter
from decimal import Decimal


class GetAllEventsTestCase(APITestCase):

    """
    Separate class for getting one or all events
    """

    def setUp(self):
        '''Initial data'''

        example_date = datetime.datetime(2018, 7, 29, 12, 0, 13, tzinfo=pytz.UTC)
        new_event = Event(name='Test event', date=example_date)
        new_event.save()
        new_event_1 = Event(name='Test event 2', date=example_date)
        new_event_1.save()

    def test_get_one_event(self):
        '''Get one event'''

        data = {'name': 'Test event 2'}

        response = self.client.generic(method='GET',
                path='/event/2/', data=json.dumps(data),
                content_type='application/json')

        correct_response = {'id': 2, 'name': 'Test event 2',
                            'date': '2018-07-29T14:00:13+02:00'}

        self.assertEqual(response.data, correct_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_events(self):
        '''Get all events'''

        data = {}
        response = self.client.generic(method='GET', path='/event/'
                , data=json.dumps(data), content_type='application/json'
                )

        correct_response = [collections.OrderedDict({'id': 1,
                            'name': 'Test event',
                            'date': '2018-07-29T14:00:13+02:00'}),
                            collections.OrderedDict({'id': 2,
                            'name': 'Test event 2',
                            'date': '2018-07-29T14:00:13+02:00'})]

        self.assertEqual(response.data, correct_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_event_errror(self):
        '''Get one event error'''

        data = {'name': 'Test event 3'}
        response = self.client.generic(method='GET',
                path='/new_events/3/', data=json.dumps(data),
                content_type='application/json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)


class GetAvaiableTickets(APITestCase):

    """
    Separate class for getting all avaiable tickets
    """

    def setUp(self):
        '''Initial data'''

        example_date = datetime.datetime(2018, 7, 29, 12, 0, 13, tzinfo=pytz.UTC)
        new_event = Event(name='Test event', date=example_date)
        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='regular',
                                    price=55.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='budget',
                                   price=45.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='premium',
                                    price=95.00)
            ticket_premium.save()
            ticket_VIP = Ticket(event=new_event, type='vip',
                                price=155.00)
            ticket_VIP.save()

    def test_get_all_tickets(self):
        '''Get all tickets'''

        data = {'id': '1'}
        response = self.client.generic(method='GET', path='/tickets/',
                data=json.dumps(data), content_type='application/json')
        correct_response = {
            'regular': 10,
            'budget': 10,
            'premium': 10,
            'vip': 10,
            }

        self.assertEqual(response.data, correct_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_tickets_one_sold(self):
        '''Get all tickets but one is sold'''
       
        single_event = Event.objects.get(name='Test event')
        tickets = Ticket.objects.filter(event=single_event)
        sell_ticket = tickets[0]
        sell_ticket.sold_status = True
        sell_ticket.save()

        all_types = tickets.values_list('type', flat=True)
        avaiable_tickets = {}
        for i in all_types:
            avaiable_tickets[i] = 0
        for ticket in tickets:
            if ticket.sold_status is False:
                avaiable_tickets[ticket.type] += 1
        correct_response = {
            'regular': 9,
            'budget': 10,
            'premium': 10,
            'vip': 10,
            }
        data = {'id': '1'}
        response = self.client.generic(method='GET', path='/tickets/',
                data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.data, correct_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_event_errror(self):
        '''Get tickets error'''

        data = {'id': '7'}
        response = self.client.generic(method='GET', path='/tickets/',
                data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)


class MakeReservationTest(APITestCase):

    def setUp(self):
        '''Initial data'''

        example_date = datetime.datetime(2018, 7, 29, 12, 0, 13, tzinfo=pytz.UTC)
        new_event = Event(name='Test event', date=example_date)

        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='regular',
                                    price=55.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='budget',
                                   price=45.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='premium',
                                    price=95.00)
            ticket_premium.save()

    def test_correct_reservation(self):
        '''Reserve ticket '''
        data = {"ticket_type":"budget", "event_id":1}
        response = self.client.put(data=data ,path='/reserve_ticket/')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_no_vip_ticket(self):
        '''Reserve ticket but no ticket'''
        data = {"ticket_type":"VIP", "event_id":1}
        response = self.client.put(data = data,path='/reserve_ticket/')

        self.assertEqual(response.status_code,
                         status.HTTP_417_EXPECTATION_FAILED)

    def test_no_event(self):
        '''Reserve ticket but no event '''
        data = {"ticket_type":"budget", "event_id":7}
        response = self.client.put(data = data,path='/reserve_ticket/')

        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)


class PaymentTest(APITestCase):

    def setUp(self):
        '''Initial data'''

        example_date = datetime.datetime( 2018, 7, 29, 12, 0, 13, tzinfo=pytz.UTC)
        new_event = Event(name='Test event', date=example_date)
        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='regular',
                                    price=55.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='budget',
                                   price=45.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='premium',
                                    price=95.00)
            ticket_premium.save()

    def test_correct_payment(self):
        '''Pay for ticket'''
        
        data={"ticket_type":"premium", "event_id":1}
        reservation = self.client.put(data = data,path='/reserve_ticket/')
        ticket_number = reservation.data['ticket_id']
        data = {'ticket_id': ticket_number}
        response = self.client.put(path='/payment/',
                                   data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reservation_lost(self):
        '''Pay for ticket but there is no reservation'''
        data = {'ticket_id': 5}
        response = self.client.put(path='/payment/',
                                   data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)


class GetReservationNumber(APITestCase):

    def setUp(self):
        '''Initial data'''
        
        example_date = datetime.datetime(2018, 7, 29, 12, 0, 13, tzinfo=pytz.UTC)
        new_event = Event(name='Test event', date=example_date)
        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='regular',
                                    price=55.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='budget',
                                   price=45.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='premium',
                                    price=95.00)
            ticket_premium.save()

    def test_get_reservation_number(self):
        '''Get reervation information '''

        data={"ticket_type":"premium", "event_id":1}
        reservation = self.client.put(data = data,path='/reserve_ticket/')
        ticket_number = reservation.data['ticket_id']
        pay = self.client.put(path='/payment/',
                              data=json.dumps({'ticket_id': ticket_number}),
                              content_type='application/json')

        data = {'reservation_number': pay.data['reservation_number']}
        reservation_number = self.client.generic(method='GET',
                path='/status/', data=json.dumps(data),
                content_type='application/json')

        self.assertEqual(reservation_number.status_code,
                         status.HTTP_200_OK)

    def test_wrong_reservation_number(self):
        '''Get reervation information, wrong number '''
        data = {'reservation_number': 'N7VQVVQE8RJCOMJZZXNLZFS0V'}
        reservation_number = self.client.generic(method='GET',
                path='/status/', data=json.dumps(data),
                content_type='application/json')

        self.assertEqual(reservation_number.status_code,
                         status.HTTP_404_NOT_FOUND)


class GetStatisticsTest(APITestCase):

    def setUp(self):
        '''Initial data'''

        example_date = datetime.datetime( 2018, 7, 29, 12, 0, 13, tzinfo=pytz.UTC)
        new_event = Event(name='Test event_1', date=example_date)
        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='regular',
                                    price=10.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='budget',
                                   price=35.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='premium',
                                    price=155.00)
            ticket_premium.save()

        new_event = Event(name='Test event_2', date=example_date)
        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='regular',
                                    price=55.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='budget',
                                   price=45.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='premium',
                                    price=285.00)
            ticket_premium.save()
            ticket_premium = Ticket(event=new_event, type='vip',
                                    price=195.00)
            ticket_premium.save()

        new_event = Event(name='Test event_3', date=example_date)
        new_event.save()
        for i in range(10):
            ticket_regular = Ticket(event=new_event, type='regular',
                                    price=25.00)
            ticket_regular.save()
            ticket_budget = Ticket(event=new_event, type='budget',
                                   price=35.00)
            ticket_budget.save()
            ticket_premium = Ticket(event=new_event, type='vip',
                                    price=95.00)
            ticket_premium.save()

    def test_nothing_sold(self):
        ''' No ticket was sold '''
        response = self.client.generic(method='GET', path='/statistics/'
                , content_type='application/json')
        correct_response = {
            'reserved_tickets_by_event_and_type': {'Test event_1': Counter(),
                    'Test event_2': Counter(),
                    'Test event_3': Counter()},
            'reserved_tickets_by_event': {'Test event_1': 0,
                    'Test event_2': 0, 'Test event_3': 0},
            'reserved_tickets_by_type': Counter(),
            'profit_by_event': {'Test event_1': 0, 'Test event_2': 0,
                                'Test event_3': 0},
            'event_popularity_ranking': {'Test event_1': 0.0,
                    'Test event_2': 0.0, 'Test event_3': 0.0},
            }

        self.assertEqual(response.data, correct_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sold_some_tickets(self):
        ''' Test statistic based on some sold tickets '''
        ticket_to_sell = [1, 2, 10, 26, 18, 20, 40, 44, 55, 65, 88, 89, 99, 95,
            96, 94, 93, 97, 98]
        for i in ticket_to_sell:
            ticket = Ticket.objects.get(pk=i)
            ticket.sold_status = True
            ticket.save()

            # self.client.put(path='/payment/', data=json.dumps({'ticket_id':str(i)}), content_type='application/json')

        response = self.client.generic(method='get', path='/statistics/'
                , content_type='application/json')
        correct_response = {
            'reserved_tickets_by_event_and_type': {'Test event_1': Counter({'budget': 3,
                    'regular': 2, 'premium': 1}),
                    'Test event_2': Counter({'budget': 2, 'regular': 1,
                    'premium': 1}), 'Test event_3': Counter({'vip': 3,
                    'regular': 3, 'budget': 3})},
            'reserved_tickets_by_event': {'Test event_1': 6,
                    'Test event_2': 4, 'Test event_3': 9},
            'reserved_tickets_by_type': Counter({
                'budget': 8,
                'regular': 6,
                'premium': 2,
                'vip': 3,
                }),
            'profit_by_event': {'Test event_1': Decimal('280.00'),
                                'Test event_2': Decimal('430.00'),
                                'Test event_3': Decimal('465.00')},
            'event_popularity_ranking': {'Test event_1': 0.2,
                    'Test event_2': 0.1, 'Test event_3': 0.3},
            }

        self.maxDiff = None
        self.assertEqual(response.data, correct_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
