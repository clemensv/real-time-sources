"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_earthquakes_producer_data.usgs.earthquakes.event import Event


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
            id='jjaughsqkbmisdwzeqil',
            magnitude=float(98.20719726717499),
            mag_type='njrrfeznjuodfxomspvh',
            place='xgukkyhnrmlrozmlgcoq',
            event_time='uchummmhcuajvhvaxbmy',
            updated='gwznpttyocyfnhjbagjc',
            url='pqmhkoxgdckejlemajcl',
            detail_url='gjquejmwofsxwimvshrs',
            felt=int(5),
            cdi=float(95.00091540971579),
            mmi=float(94.84994138589062),
            alert='giuwjslfxkouztenusdn',
            status='hbvdvckvvmhbyddqzldj',
            tsunami=int(17),
            sig=int(76),
            net='ilhppyipitjsamzuyjsr',
            code='mmuyykqjryttgeerbvwd',
            sources='uvhibnqklnztihwqifih',
            nst=int(16),
            dmin=float(48.05307085526146),
            rms=float(83.23381490248467),
            gap=float(69.45479631315663),
            event_type='fzbkigvxrsndfvoulgqu',
            latitude=float(11.735219636003414),
            longitude=float(12.11533737653877),
            depth=float(65.18769955315157),
            magnitude_bucket='bzeepzhuywqorchfekvb'
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'jjaughsqkbmisdwzeqil'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = float(98.20719726717499)
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_mag_type_property(self):
        """
        Test mag_type property
        """
        test_value = 'njrrfeznjuodfxomspvh'
        self.instance.mag_type = test_value
        self.assertEqual(self.instance.mag_type, test_value)
    
    def test_place_property(self):
        """
        Test place property
        """
        test_value = 'xgukkyhnrmlrozmlgcoq'
        self.instance.place = test_value
        self.assertEqual(self.instance.place, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'uchummmhcuajvhvaxbmy'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'gwznpttyocyfnhjbagjc'
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'pqmhkoxgdckejlemajcl'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_detail_url_property(self):
        """
        Test detail_url property
        """
        test_value = 'gjquejmwofsxwimvshrs'
        self.instance.detail_url = test_value
        self.assertEqual(self.instance.detail_url, test_value)
    
    def test_felt_property(self):
        """
        Test felt property
        """
        test_value = int(5)
        self.instance.felt = test_value
        self.assertEqual(self.instance.felt, test_value)
    
    def test_cdi_property(self):
        """
        Test cdi property
        """
        test_value = float(95.00091540971579)
        self.instance.cdi = test_value
        self.assertEqual(self.instance.cdi, test_value)
    
    def test_mmi_property(self):
        """
        Test mmi property
        """
        test_value = float(94.84994138589062)
        self.instance.mmi = test_value
        self.assertEqual(self.instance.mmi, test_value)
    
    def test_alert_property(self):
        """
        Test alert property
        """
        test_value = 'giuwjslfxkouztenusdn'
        self.instance.alert = test_value
        self.assertEqual(self.instance.alert, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'hbvdvckvvmhbyddqzldj'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_tsunami_property(self):
        """
        Test tsunami property
        """
        test_value = int(17)
        self.instance.tsunami = test_value
        self.assertEqual(self.instance.tsunami, test_value)
    
    def test_sig_property(self):
        """
        Test sig property
        """
        test_value = int(76)
        self.instance.sig = test_value
        self.assertEqual(self.instance.sig, test_value)
    
    def test_net_property(self):
        """
        Test net property
        """
        test_value = 'ilhppyipitjsamzuyjsr'
        self.instance.net = test_value
        self.assertEqual(self.instance.net, test_value)
    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'mmuyykqjryttgeerbvwd'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_sources_property(self):
        """
        Test sources property
        """
        test_value = 'uvhibnqklnztihwqifih'
        self.instance.sources = test_value
        self.assertEqual(self.instance.sources, test_value)
    
    def test_nst_property(self):
        """
        Test nst property
        """
        test_value = int(16)
        self.instance.nst = test_value
        self.assertEqual(self.instance.nst, test_value)
    
    def test_dmin_property(self):
        """
        Test dmin property
        """
        test_value = float(48.05307085526146)
        self.instance.dmin = test_value
        self.assertEqual(self.instance.dmin, test_value)
    
    def test_rms_property(self):
        """
        Test rms property
        """
        test_value = float(83.23381490248467)
        self.instance.rms = test_value
        self.assertEqual(self.instance.rms, test_value)
    
    def test_gap_property(self):
        """
        Test gap property
        """
        test_value = float(69.45479631315663)
        self.instance.gap = test_value
        self.assertEqual(self.instance.gap, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'fzbkigvxrsndfvoulgqu'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(11.735219636003414)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(12.11533737653877)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(65.18769955315157)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_magnitude_bucket_property(self):
        """
        Test magnitude_bucket property
        """
        test_value = 'bzeepzhuywqorchfekvb'
        self.instance.magnitude_bucket = test_value
        self.assertEqual(self.instance.magnitude_bucket, test_value)
    
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

