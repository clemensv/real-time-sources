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
            id='xdvmsufyzafyfofivlwn',
            magnitude=float(79.51195619045833),
            magnitude_bucket='efliciyzyqdudjbnldsz',
            mag_type='tyztpfsdnesqazdwfcnp',
            place='nspfjkvoudknoytxjpdj',
            event_time='vohxbixldltvwyovkhbm',
            updated='anktoasmipsghanmcctw',
            url='rhignicwzukbibwedjbz',
            detail_url='jghgmewqhjdzhwcvdtbd',
            felt=int(5),
            cdi=float(23.486302746866617),
            mmi=float(42.21776453599817),
            alert='vradkzonctwxwxmvwszn',
            status='jdvdbcfrpsyxmaxnuqcf',
            tsunami=int(92),
            sig=int(15),
            net='hrcvzodqfujdautlqgeb',
            code='wogwchuntnecflcpfout',
            sources='etgnptdckworurqpqvyi',
            nst=int(82),
            dmin=float(79.31082839478691),
            rms=float(99.82490247325461),
            gap=float(25.6111615006794),
            event_type='ekgxmengsmkdhxpwhfme',
            latitude=float(83.55134839723495),
            longitude=float(17.668074771198437),
            depth=float(89.94569028133614)
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'xdvmsufyzafyfofivlwn'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = float(79.51195619045833)
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_magnitude_bucket_property(self):
        """
        Test magnitude_bucket property
        """
        test_value = 'efliciyzyqdudjbnldsz'
        self.instance.magnitude_bucket = test_value
        self.assertEqual(self.instance.magnitude_bucket, test_value)
    
    def test_mag_type_property(self):
        """
        Test mag_type property
        """
        test_value = 'tyztpfsdnesqazdwfcnp'
        self.instance.mag_type = test_value
        self.assertEqual(self.instance.mag_type, test_value)
    
    def test_place_property(self):
        """
        Test place property
        """
        test_value = 'nspfjkvoudknoytxjpdj'
        self.instance.place = test_value
        self.assertEqual(self.instance.place, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'vohxbixldltvwyovkhbm'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'anktoasmipsghanmcctw'
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'rhignicwzukbibwedjbz'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_detail_url_property(self):
        """
        Test detail_url property
        """
        test_value = 'jghgmewqhjdzhwcvdtbd'
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
        test_value = float(23.486302746866617)
        self.instance.cdi = test_value
        self.assertEqual(self.instance.cdi, test_value)
    
    def test_mmi_property(self):
        """
        Test mmi property
        """
        test_value = float(42.21776453599817)
        self.instance.mmi = test_value
        self.assertEqual(self.instance.mmi, test_value)
    
    def test_alert_property(self):
        """
        Test alert property
        """
        test_value = 'vradkzonctwxwxmvwszn'
        self.instance.alert = test_value
        self.assertEqual(self.instance.alert, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'jdvdbcfrpsyxmaxnuqcf'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_tsunami_property(self):
        """
        Test tsunami property
        """
        test_value = int(92)
        self.instance.tsunami = test_value
        self.assertEqual(self.instance.tsunami, test_value)
    
    def test_sig_property(self):
        """
        Test sig property
        """
        test_value = int(15)
        self.instance.sig = test_value
        self.assertEqual(self.instance.sig, test_value)
    
    def test_net_property(self):
        """
        Test net property
        """
        test_value = 'hrcvzodqfujdautlqgeb'
        self.instance.net = test_value
        self.assertEqual(self.instance.net, test_value)
    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'wogwchuntnecflcpfout'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_sources_property(self):
        """
        Test sources property
        """
        test_value = 'etgnptdckworurqpqvyi'
        self.instance.sources = test_value
        self.assertEqual(self.instance.sources, test_value)
    
    def test_nst_property(self):
        """
        Test nst property
        """
        test_value = int(82)
        self.instance.nst = test_value
        self.assertEqual(self.instance.nst, test_value)
    
    def test_dmin_property(self):
        """
        Test dmin property
        """
        test_value = float(79.31082839478691)
        self.instance.dmin = test_value
        self.assertEqual(self.instance.dmin, test_value)
    
    def test_rms_property(self):
        """
        Test rms property
        """
        test_value = float(99.82490247325461)
        self.instance.rms = test_value
        self.assertEqual(self.instance.rms, test_value)
    
    def test_gap_property(self):
        """
        Test gap property
        """
        test_value = float(25.6111615006794)
        self.instance.gap = test_value
        self.assertEqual(self.instance.gap, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'ekgxmengsmkdhxpwhfme'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(83.55134839723495)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(17.668074771198437)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(89.94569028133614)
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
