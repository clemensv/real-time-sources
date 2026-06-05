"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from billetto_mqtt_producer_data.event import Event


class Test_Event(unittest.TestCase):
    """
    Test case for Event
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Event.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Event for testing
        """
        instance = Event(
            event_id=int(100),
            title='bxwkfkjsaxmliyoqyeht',
            description='lgthtdicizbjqkrfuszu',
            startdate='hfvhiztjpiwskaxrieoc',
            enddate='bbjpypkvphbxjtpbzhwh',
            url='vtqusjswdstumxghjiuc',
            image_link='nawpfzaezzthfsbwwvbo',
            status='fhyenecvhgmfuakiuyks',
            location_city='tsmhodoncagoawbbonfd',
            location_name='xxktzbqviftqfpxapbwh',
            location_address='qtvdlkxijeonoqlnllif',
            location_zip_code='gelaypvvovtadiadjlug',
            location_country_code='jbjeptcvtljkffhuypav',
            location_latitude=float(12.51689496946029),
            location_longitude=float(3.678417532802236),
            organiser_id=int(24),
            organiser_name='kqipcdrsljyseutmfhvv',
            minimum_price_amount_in_cents=int(44),
            minimum_price_currency='uusqanxkqlyhwvdzvxuf',
            availability='rrhjqhzfvlktcmjqaadf'
        )
        return instance

    
    def test_event_id_property(self):
        """
        Test event_id property
        """
        test_value = int(100)
        self.instance.event_id = test_value
        self.assertEqual(self.instance.event_id, test_value)
    
    def test_title_property(self):
        """
        Test title property
        """
        test_value = 'bxwkfkjsaxmliyoqyeht'
        self.instance.title = test_value
        self.assertEqual(self.instance.title, test_value)
    
    def test_description_property(self):
        """
        Test description property
        """
        test_value = 'lgthtdicizbjqkrfuszu'
        self.instance.description = test_value
        self.assertEqual(self.instance.description, test_value)
    
    def test_startdate_property(self):
        """
        Test startdate property
        """
        test_value = 'hfvhiztjpiwskaxrieoc'
        self.instance.startdate = test_value
        self.assertEqual(self.instance.startdate, test_value)
    
    def test_enddate_property(self):
        """
        Test enddate property
        """
        test_value = 'bbjpypkvphbxjtpbzhwh'
        self.instance.enddate = test_value
        self.assertEqual(self.instance.enddate, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'vtqusjswdstumxghjiuc'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_image_link_property(self):
        """
        Test image_link property
        """
        test_value = 'nawpfzaezzthfsbwwvbo'
        self.instance.image_link = test_value
        self.assertEqual(self.instance.image_link, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'fhyenecvhgmfuakiuyks'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_location_city_property(self):
        """
        Test location_city property
        """
        test_value = 'tsmhodoncagoawbbonfd'
        self.instance.location_city = test_value
        self.assertEqual(self.instance.location_city, test_value)
    
    def test_location_name_property(self):
        """
        Test location_name property
        """
        test_value = 'xxktzbqviftqfpxapbwh'
        self.instance.location_name = test_value
        self.assertEqual(self.instance.location_name, test_value)
    
    def test_location_address_property(self):
        """
        Test location_address property
        """
        test_value = 'qtvdlkxijeonoqlnllif'
        self.instance.location_address = test_value
        self.assertEqual(self.instance.location_address, test_value)
    
    def test_location_zip_code_property(self):
        """
        Test location_zip_code property
        """
        test_value = 'gelaypvvovtadiadjlug'
        self.instance.location_zip_code = test_value
        self.assertEqual(self.instance.location_zip_code, test_value)
    
    def test_location_country_code_property(self):
        """
        Test location_country_code property
        """
        test_value = 'jbjeptcvtljkffhuypav'
        self.instance.location_country_code = test_value
        self.assertEqual(self.instance.location_country_code, test_value)
    
    def test_location_latitude_property(self):
        """
        Test location_latitude property
        """
        test_value = float(12.51689496946029)
        self.instance.location_latitude = test_value
        self.assertEqual(self.instance.location_latitude, test_value)
    
    def test_location_longitude_property(self):
        """
        Test location_longitude property
        """
        test_value = float(3.678417532802236)
        self.instance.location_longitude = test_value
        self.assertEqual(self.instance.location_longitude, test_value)
    
    def test_organiser_id_property(self):
        """
        Test organiser_id property
        """
        test_value = int(24)
        self.instance.organiser_id = test_value
        self.assertEqual(self.instance.organiser_id, test_value)
    
    def test_organiser_name_property(self):
        """
        Test organiser_name property
        """
        test_value = 'kqipcdrsljyseutmfhvv'
        self.instance.organiser_name = test_value
        self.assertEqual(self.instance.organiser_name, test_value)
    
    def test_minimum_price_amount_in_cents_property(self):
        """
        Test minimum_price_amount_in_cents property
        """
        test_value = int(44)
        self.instance.minimum_price_amount_in_cents = test_value
        self.assertEqual(self.instance.minimum_price_amount_in_cents, test_value)
    
    def test_minimum_price_currency_property(self):
        """
        Test minimum_price_currency property
        """
        test_value = 'uusqanxkqlyhwvdzvxuf'
        self.instance.minimum_price_currency = test_value
        self.assertEqual(self.instance.minimum_price_currency, test_value)
    
    def test_availability_property(self):
        """
        Test availability property
        """
        test_value = 'rrhjqhzfvlktcmjqaadf'
        self.instance.availability = test_value
        self.assertEqual(self.instance.availability, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Event.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Event.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

