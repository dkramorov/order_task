# -*- coding:utf-8 -*-
import time
import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count
from django.db import connections

from order.models import Order, OrderItem
from catalogue.models import Product

class Command(BaseCommand):
    """
    """
    def add_arguments(self, parser):
        parser.add_argument('--folder',
            action = 'store',
            dest = 'folder',
            type = str,
            default = False,
            help = 'Set folder with spinner files')
        parser.add_argument('--catalogue',
            action = 'store_true',
            dest = 'catalogue',
            default = False,
            help = 'Load catalogue')

    def handle(self, *args, **options):
        now = time.time()

        #a = Order.objects.all().last()
        #print(a.history.all()[0].get_all_data())
        #exit()

        session = requests.Session()
        session.auth = ('jocker', 'reabhxbr')

        params = {
            'name': 'Test_%s' % now,
            'code': 'test_%s' % now,
            'price': '103.00',
        }
        new_user = session.post('http://127.0.0.1:8000/api/product/', json=params)
        print(new_user.json())

        params = {
            'order': 2,
            'product': 1,
            'amount': 2,
        }

        #new_order_item = session.post('http://127.0.0.1:8000/api/order_item/', json=params)
        #print(new_order_item.json())

        params = {
            'items': [],
        }

        new_order = session.post('http://127.0.0.1:8000/api/order/', json=params)
        print(new_order.text)
