"""
Test case for CapInfo
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from cap_alerts_producer_data.org.oasis.cap.alerts.capinfo import CapInfo
from cap_alerts_producer_data.org.oasis.cap.alerts.valuepair import ValuePair
from cap_alerts_producer_data.org.oasis.cap.alerts.caparea import CapArea
from cap_alerts_producer_data.org.oasis.cap.alerts.certaintyenum import CertaintyEnum
from cap_alerts_producer_data.org.oasis.cap.alerts.severityenum import SeverityEnum
from cap_alerts_producer_data.org.oasis.cap.alerts.categorylistenum import CategoryListEnum
from cap_alerts_producer_data.org.oasis.cap.alerts.capresource import CapResource
from cap_alerts_producer_data.org.oasis.cap.alerts.responsetypelistenum import ResponseTypelistenum
from cap_alerts_producer_data.org.oasis.cap.alerts.urgencyenum import UrgencyEnum
import datetime


class Test_CapInfo(unittest.TestCase):
    """
    Test case for CapInfo
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_CapInfo.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of CapInfo for testing
        """
        instance = CapInfo(
            language='blqqxcxywctwnwfrtkfi',
            category=[CategoryListEnum.Geo, CategoryListEnum.Geo],
            event='yqbmfeeytvhnjhrhjtlt',
            response_type=[ResponseTypelistenum.Shelter, ResponseTypelistenum.Shelter, ResponseTypelistenum.Shelter, ResponseTypelistenum.Shelter],
            urgency=UrgencyEnum.Immediate,
            severity=SeverityEnum.Extreme,
            certainty=CertaintyEnum.Observed,
            audience='fcoblzeayeedhmtbfvbw',
            event_code=[None, None],
            effective=datetime.datetime.now(datetime.timezone.utc),
            onset=datetime.datetime.now(datetime.timezone.utc),
            expires=datetime.datetime.now(datetime.timezone.utc),
            sender_name='xrpvqgybvifkxrchjahk',
            headline='verinvpinowumhhttywc',
            description='glyhbymwxjeqxflvhrxz',
            instruction='zgoeunjndowbpelinecy',
            web='ofkigksfydgvqpfsmuuq',
            contact='ainkagpdzrvjxpahyxep',
            parameter=[None, None, None, None, None],
            resource=[None, None, None, None],
            area=[None, None, None],
            ends=datetime.datetime.now(datetime.timezone.utc)
        )
        return instance

    
    def test_language_property(self):
        """
        Test language property
        """
        test_value = 'blqqxcxywctwnwfrtkfi'
        self.instance.language = test_value
        self.assertEqual(self.instance.language, test_value)
    
    def test_category_property(self):
        """
        Test category property
        """
        test_value = [CategoryListEnum.Geo, CategoryListEnum.Geo]
        self.instance.category = test_value
        self.assertEqual(self.instance.category, test_value)
    
    def test_event_property(self):
        """
        Test event property
        """
        test_value = 'yqbmfeeytvhnjhrhjtlt'
        self.instance.event = test_value
        self.assertEqual(self.instance.event, test_value)
    
    def test_response_type_property(self):
        """
        Test response_type property
        """
        test_value = [ResponseTypelistenum.Shelter, ResponseTypelistenum.Shelter, ResponseTypelistenum.Shelter, ResponseTypelistenum.Shelter]
        self.instance.response_type = test_value
        self.assertEqual(self.instance.response_type, test_value)
    
    def test_urgency_property(self):
        """
        Test urgency property
        """
        test_value = UrgencyEnum.Immediate
        self.instance.urgency = test_value
        self.assertEqual(self.instance.urgency, test_value)
    
    def test_severity_property(self):
        """
        Test severity property
        """
        test_value = SeverityEnum.Extreme
        self.instance.severity = test_value
        self.assertEqual(self.instance.severity, test_value)
    
    def test_certainty_property(self):
        """
        Test certainty property
        """
        test_value = CertaintyEnum.Observed
        self.instance.certainty = test_value
        self.assertEqual(self.instance.certainty, test_value)
    
    def test_audience_property(self):
        """
        Test audience property
        """
        test_value = 'fcoblzeayeedhmtbfvbw'
        self.instance.audience = test_value
        self.assertEqual(self.instance.audience, test_value)
    
    def test_event_code_property(self):
        """
        Test event_code property
        """
        test_value = [None, None]
        self.instance.event_code = test_value
        self.assertEqual(self.instance.event_code, test_value)
    
    def test_effective_property(self):
        """
        Test effective property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.effective = test_value
        self.assertEqual(self.instance.effective, test_value)
    
    def test_onset_property(self):
        """
        Test onset property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.onset = test_value
        self.assertEqual(self.instance.onset, test_value)
    
    def test_expires_property(self):
        """
        Test expires property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.expires = test_value
        self.assertEqual(self.instance.expires, test_value)
    
    def test_sender_name_property(self):
        """
        Test sender_name property
        """
        test_value = 'xrpvqgybvifkxrchjahk'
        self.instance.sender_name = test_value
        self.assertEqual(self.instance.sender_name, test_value)
    
    def test_headline_property(self):
        """
        Test headline property
        """
        test_value = 'verinvpinowumhhttywc'
        self.instance.headline = test_value
        self.assertEqual(self.instance.headline, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'glyhbymwxjeqxflvhrxz'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_instruction_property(self):
        """
        Test instruction property
        """
        test_value = 'zgoeunjndowbpelinecy'
        self.instance.instruction = test_value
        self.assertEqual(self.instance.instruction, test_value)
    
    def test_web_property(self):
        """
        Test web property
        """
        test_value = 'ofkigksfydgvqpfsmuuq'
        self.instance.web = test_value
        self.assertEqual(self.instance.web, test_value)
    
    def test_contact_property(self):
        """
        Test contact property
        """
        test_value = 'ainkagpdzrvjxpahyxep'
        self.instance.contact = test_value
        self.assertEqual(self.instance.contact, test_value)
    
    def test_parameter_property(self):
        """
        Test parameter property
        """
        test_value = [None, None, None, None, None]
        self.instance.parameter = test_value
        self.assertEqual(self.instance.parameter, test_value)
    
    def test_resource_property(self):
        """
        Test resource property
        """
        test_value = [None, None, None, None]
        self.instance.resource = test_value
        self.assertEqual(self.instance.resource, test_value)
    
    def test_area_property(self):
        """
        Test area property
        """
        test_value = [None, None, None]
        self.instance.area = test_value
        self.assertEqual(self.instance.area, test_value)
    
    def test_ends_property(self):
        """
        Test ends property
        """
        test_value = datetime.datetime.now(datetime.timezone.utc)
        self.instance.ends = test_value
        self.assertEqual(self.instance.ends, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = CapInfo.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = CapInfo.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

