"""
Test case for Event
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from usgs_earthquakes_amqp_producer_data.usgs.earthquakes.event import Event


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
            id='cqcgsihddfiakutuvybe',
            magnitude=float(92.93584006786328),
            mag_type='gdrrkcrkhshkwkxsgvkd',
            place='kggfyzdvxbzskscijjwd',
            event_time='qiibsbqrpqwagakmjmrr',
            updated='yqxkxfuwhmdgwefnhoej',
            url='ynlhjyeisozulqzehriy',
            detail_url='wntuozidlrzmfchlvkul',
            felt=int(23),
            cdi=float(55.42896585063455),
            mmi=float(4.048958443489381),
            alert='ajtsqqzgosatqnjhthqd',
            status='idazysgraedyvqzcgdtx',
            tsunami=int(94),
            sig=int(95),
            net='wtzxravacigxqtvxgihb',
            code='meehgfmoxmxagwjoqlpd',
            sources='xkspjkvbgpvxluvzdbhp',
            nst=int(72),
            dmin=float(11.409522717966913),
            rms=float(19.900592687074294),
            gap=float(67.69936265623005),
            event_type='zftzmhjfoqylwbcxiszq',
            latitude=float(82.26714431884649),
            longitude=float(12.40054305839836),
            depth=float(67.09075333343371),
            magnitude_bucket='atfaggpctrtjtogbwnmy'
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'cqcgsihddfiakutuvybe'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = float(92.93584006786328)
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_mag_type_property(self):
        """
        Test mag_type property
        """
        test_value = 'gdrrkcrkhshkwkxsgvkd'
        self.instance.mag_type = test_value
        self.assertEqual(self.instance.mag_type, test_value)
    
    def test_place_property(self):
        """
        Test place property
        """
        test_value = 'kggfyzdvxbzskscijjwd'
        self.instance.place = test_value
        self.assertEqual(self.instance.place, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'qiibsbqrpqwagakmjmrr'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'yqxkxfuwhmdgwefnhoej'
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'ynlhjyeisozulqzehriy'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_detail_url_property(self):
        """
        Test detail_url property
        """
        test_value = 'wntuozidlrzmfchlvkul'
        self.instance.detail_url = test_value
        self.assertEqual(self.instance.detail_url, test_value)
    
    def test_felt_property(self):
        """
        Test felt property
        """
        test_value = int(23)
        self.instance.felt = test_value
        self.assertEqual(self.instance.felt, test_value)
    
    def test_cdi_property(self):
        """
        Test cdi property
        """
        test_value = float(55.42896585063455)
        self.instance.cdi = test_value
        self.assertEqual(self.instance.cdi, test_value)
    
    def test_mmi_property(self):
        """
        Test mmi property
        """
        test_value = float(4.048958443489381)
        self.instance.mmi = test_value
        self.assertEqual(self.instance.mmi, test_value)
    
    def test_alert_property(self):
        """
        Test alert property
        """
        test_value = 'ajtsqqzgosatqnjhthqd'
        self.instance.alert = test_value
        self.assertEqual(self.instance.alert, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'idazysgraedyvqzcgdtx'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_tsunami_property(self):
        """
        Test tsunami property
        """
        test_value = int(94)
        self.instance.tsunami = test_value
        self.assertEqual(self.instance.tsunami, test_value)
    
    def test_sig_property(self):
        """
        Test sig property
        """
        test_value = int(95)
        self.instance.sig = test_value
        self.assertEqual(self.instance.sig, test_value)
    
    def test_net_property(self):
        """
        Test net property
        """
        test_value = 'wtzxravacigxqtvxgihb'
        self.instance.net = test_value
        self.assertEqual(self.instance.net, test_value)
    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'meehgfmoxmxagwjoqlpd'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_sources_property(self):
        """
        Test sources property
        """
        test_value = 'xkspjkvbgpvxluvzdbhp'
        self.instance.sources = test_value
        self.assertEqual(self.instance.sources, test_value)
    
    def test_nst_property(self):
        """
        Test nst property
        """
        test_value = int(72)
        self.instance.nst = test_value
        self.assertEqual(self.instance.nst, test_value)
    
    def test_dmin_property(self):
        """
        Test dmin property
        """
        test_value = float(11.409522717966913)
        self.instance.dmin = test_value
        self.assertEqual(self.instance.dmin, test_value)
    
    def test_rms_property(self):
        """
        Test rms property
        """
        test_value = float(19.900592687074294)
        self.instance.rms = test_value
        self.assertEqual(self.instance.rms, test_value)
    
    def test_gap_property(self):
        """
        Test gap property
        """
        test_value = float(67.69936265623005)
        self.instance.gap = test_value
        self.assertEqual(self.instance.gap, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'zftzmhjfoqylwbcxiszq'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(82.26714431884649)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(12.40054305839836)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(67.09075333343371)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_magnitude_bucket_property(self):
        """
        Test magnitude_bucket property
        """
        test_value = 'atfaggpctrtjtogbwnmy'
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

