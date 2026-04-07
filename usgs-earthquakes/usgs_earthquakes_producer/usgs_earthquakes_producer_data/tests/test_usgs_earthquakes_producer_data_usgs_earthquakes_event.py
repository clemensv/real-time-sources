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
            id='zbnevtekwclfjcpdqnpk',
            magnitude=float(15.461559239610622),
            mag_type='ywnvczfdkebikzmdzqie',
            place='bvjxzybjfmbmyuvpcfan',
            event_time='lejdohobdevlobwlrtwa',
            updated='droljpnynzfbdjmekpqi',
            url='xzmjtehfeamwvjmvfpma',
            detail_url='jzhmvbbycdpjwwjpwnup',
            felt=int(29),
            cdi=float(98.21812568934311),
            mmi=float(23.630473022094733),
            alert='towbpwbmhwjmtsbohwvh',
            status='sfqdgwzvkknoatpoukzq',
            tsunami=int(48),
            sig=int(9),
            net='cbyfgwgijhrtehludyut',
            code='iguifpkqhahnvamqicpv',
            sources='rmahtkwgtcmkukpzibne',
            nst=int(74),
            dmin=float(8.66497801210282),
            rms=float(92.2038841270635),
            gap=float(54.22873830628265),
            event_type='iklgiuaqjhefadbvihaf',
            latitude=float(19.25264067202207),
            longitude=float(93.42897992539004),
            depth=float(74.10737770870067)
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'zbnevtekwclfjcpdqnpk'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = float(15.461559239610622)
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_mag_type_property(self):
        """
        Test mag_type property
        """
        test_value = 'ywnvczfdkebikzmdzqie'
        self.instance.mag_type = test_value
        self.assertEqual(self.instance.mag_type, test_value)
    
    def test_place_property(self):
        """
        Test place property
        """
        test_value = 'bvjxzybjfmbmyuvpcfan'
        self.instance.place = test_value
        self.assertEqual(self.instance.place, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'lejdohobdevlobwlrtwa'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'droljpnynzfbdjmekpqi'
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'xzmjtehfeamwvjmvfpma'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_detail_url_property(self):
        """
        Test detail_url property
        """
        test_value = 'jzhmvbbycdpjwwjpwnup'
        self.instance.detail_url = test_value
        self.assertEqual(self.instance.detail_url, test_value)
    
    def test_felt_property(self):
        """
        Test felt property
        """
        test_value = int(29)
        self.instance.felt = test_value
        self.assertEqual(self.instance.felt, test_value)
    
    def test_cdi_property(self):
        """
        Test cdi property
        """
        test_value = float(98.21812568934311)
        self.instance.cdi = test_value
        self.assertEqual(self.instance.cdi, test_value)
    
    def test_mmi_property(self):
        """
        Test mmi property
        """
        test_value = float(23.630473022094733)
        self.instance.mmi = test_value
        self.assertEqual(self.instance.mmi, test_value)
    
    def test_alert_property(self):
        """
        Test alert property
        """
        test_value = 'towbpwbmhwjmtsbohwvh'
        self.instance.alert = test_value
        self.assertEqual(self.instance.alert, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'sfqdgwzvkknoatpoukzq'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_tsunami_property(self):
        """
        Test tsunami property
        """
        test_value = int(48)
        self.instance.tsunami = test_value
        self.assertEqual(self.instance.tsunami, test_value)
    
    def test_sig_property(self):
        """
        Test sig property
        """
        test_value = int(9)
        self.instance.sig = test_value
        self.assertEqual(self.instance.sig, test_value)
    
    def test_net_property(self):
        """
        Test net property
        """
        test_value = 'cbyfgwgijhrtehludyut'
        self.instance.net = test_value
        self.assertEqual(self.instance.net, test_value)
    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'iguifpkqhahnvamqicpv'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_sources_property(self):
        """
        Test sources property
        """
        test_value = 'rmahtkwgtcmkukpzibne'
        self.instance.sources = test_value
        self.assertEqual(self.instance.sources, test_value)
    
    def test_nst_property(self):
        """
        Test nst property
        """
        test_value = int(74)
        self.instance.nst = test_value
        self.assertEqual(self.instance.nst, test_value)
    
    def test_dmin_property(self):
        """
        Test dmin property
        """
        test_value = float(8.66497801210282)
        self.instance.dmin = test_value
        self.assertEqual(self.instance.dmin, test_value)
    
    def test_rms_property(self):
        """
        Test rms property
        """
        test_value = float(92.2038841270635)
        self.instance.rms = test_value
        self.assertEqual(self.instance.rms, test_value)
    
    def test_gap_property(self):
        """
        Test gap property
        """
        test_value = float(54.22873830628265)
        self.instance.gap = test_value
        self.assertEqual(self.instance.gap, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'iklgiuaqjhefadbvihaf'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(19.25264067202207)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(93.42897992539004)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(74.10737770870067)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Event.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
