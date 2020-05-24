# -*- coding=utf-8 -*-
from interface.models import InterfaceJobModel
import requests


class ApiRunner:
    def __init__(self, test_plan_id):
        self.test_plan_id = test_plan_id

    def processing_plant(self, interface):
        
    def distributor(self):
        # TODO
        interfaces = InterfaceJobModel.objects.filter(test_plan_id=self.test_plan_id)
        for interface in interfaces:
