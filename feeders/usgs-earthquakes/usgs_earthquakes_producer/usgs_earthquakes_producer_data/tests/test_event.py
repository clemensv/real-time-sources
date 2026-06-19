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
            id='jlufwjcaoradcwrmiuwo',
            magnitude=float(19.940582683921082),
            mag_type='mcomaarchnbicpjuyhjv',
            place='fapgypchqyoroufmmtow',
            event_time='dzqdylqnkdfzpeivgdum',
            updated='ddmvbumxjcotnzfkjfro',
            url='ditjgwksagcaoomrkzaw',
            detail_url='qximiyhtrvbpvijtronu',
            felt=int(5),
            cdi=float(58.182755249158625),
            mmi=float(70.29498220709705),
            alert='emnkbbhukktesfgcxtjb',
            status='snolsldrlvigtxnxszfx',
            tsunami=int(62),
            sig=int(87),
            net='lklkrmtyrznrevkhikii',
            code='quolubwcvlebvvoirvzq',
            sources='jrlizwsmhzurttlesnir',
            nst=int(67),
            dmin=float(5.456161777511747),
            rms=float(72.62002631978173),
            gap=float(5.463440505137029),
            event_type='evtbyyziunuaxphcfxhi',
            latitude=float(63.29070351648256),
            longitude=float(26.797807057858737),
            depth=float(47.91926482519534),
            magnitude_bucket='lnpcqzzetfazveeuiybb'
        )
        return instance

    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'jlufwjcaoradcwrmiuwo'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_magnitude_property(self):
        """
        Test magnitude property
        """
        test_value = float(19.940582683921082)
        self.instance.magnitude = test_value
        self.assertEqual(self.instance.magnitude, test_value)
    
    def test_mag_type_property(self):
        """
        Test mag_type property
        """
        test_value = 'mcomaarchnbicpjuyhjv'
        self.instance.mag_type = test_value
        self.assertEqual(self.instance.mag_type, test_value)
    
    def test_place_property(self):
        """
        Test place property
        """
        test_value = 'fapgypchqyoroufmmtow'
        self.instance.place = test_value
        self.assertEqual(self.instance.place, test_value)
    
    def test_event_time_property(self):
        """
        Test event_time property
        """
        test_value = 'dzqdylqnkdfzpeivgdum'
        self.instance.event_time = test_value
        self.assertEqual(self.instance.event_time, test_value)
    
    def test_updated_property(self):
        """
        Test updated property
        """
        test_value = 'ddmvbumxjcotnzfkjfro'
        self.instance.updated = test_value
        self.assertEqual(self.instance.updated, test_value)
    
    def test_url_property(self):
        """
        Test url property
        """
        test_value = 'ditjgwksagcaoomrkzaw'
        self.instance.url = test_value
        self.assertEqual(self.instance.url, test_value)
    
    def test_detail_url_property(self):
        """
        Test detail_url property
        """
        test_value = 'qximiyhtrvbpvijtronu'
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
        test_value = float(58.182755249158625)
        self.instance.cdi = test_value
        self.assertEqual(self.instance.cdi, test_value)
    
    def test_mmi_property(self):
        """
        Test mmi property
        """
        test_value = float(70.29498220709705)
        self.instance.mmi = test_value
        self.assertEqual(self.instance.mmi, test_value)
    
    def test_alert_property(self):
        """
        Test alert property
        """
        test_value = 'emnkbbhukktesfgcxtjb'
        self.instance.alert = test_value
        self.assertEqual(self.instance.alert, test_value)
    
    def test_status_property(self):
        """
        Test status property
        """
        test_value = 'snolsldrlvigtxnxszfx'
        self.instance.status = test_value
        self.assertEqual(self.instance.status, test_value)
    
    def test_tsunami_property(self):
        """
        Test tsunami property
        """
        test_value = int(62)
        self.instance.tsunami = test_value
        self.assertEqual(self.instance.tsunami, test_value)
    
    def test_sig_property(self):
        """
        Test sig property
        """
        test_value = int(87)
        self.instance.sig = test_value
        self.assertEqual(self.instance.sig, test_value)
    
    def test_net_property(self):
        """
        Test net property
        """
        test_value = 'lklkrmtyrznrevkhikii'
        self.instance.net = test_value
        self.assertEqual(self.instance.net, test_value)
    
    def test_code_property(self):
        """
        Test code property
        """
        test_value = 'quolubwcvlebvvoirvzq'
        self.instance.code = test_value
        self.assertEqual(self.instance.code, test_value)
    
    def test_sources_property(self):
        """
        Test sources property
        """
        test_value = 'jrlizwsmhzurttlesnir'
        self.instance.sources = test_value
        self.assertEqual(self.instance.sources, test_value)
    
    def test_nst_property(self):
        """
        Test nst property
        """
        test_value = int(67)
        self.instance.nst = test_value
        self.assertEqual(self.instance.nst, test_value)
    
    def test_dmin_property(self):
        """
        Test dmin property
        """
        test_value = float(5.456161777511747)
        self.instance.dmin = test_value
        self.assertEqual(self.instance.dmin, test_value)
    
    def test_rms_property(self):
        """
        Test rms property
        """
        test_value = float(72.62002631978173)
        self.instance.rms = test_value
        self.assertEqual(self.instance.rms, test_value)
    
    def test_gap_property(self):
        """
        Test gap property
        """
        test_value = float(5.463440505137029)
        self.instance.gap = test_value
        self.assertEqual(self.instance.gap, test_value)
    
    def test_event_type_property(self):
        """
        Test event_type property
        """
        test_value = 'evtbyyziunuaxphcfxhi'
        self.instance.event_type = test_value
        self.assertEqual(self.instance.event_type, test_value)
    
    def test_latitude_property(self):
        """
        Test latitude property
        """
        test_value = float(63.29070351648256)
        self.instance.latitude = test_value
        self.assertEqual(self.instance.latitude, test_value)
    
    def test_longitude_property(self):
        """
        Test longitude property
        """
        test_value = float(26.797807057858737)
        self.instance.longitude = test_value
        self.assertEqual(self.instance.longitude, test_value)
    
    def test_depth_property(self):
        """
        Test depth property
        """
        test_value = float(47.91926482519534)
        self.instance.depth = test_value
        self.assertEqual(self.instance.depth, test_value)
    
    def test_magnitude_bucket_property(self):
        """
        Test magnitude_bucket property
        """
        test_value = 'lnpcqzzetfazveeuiybb'
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

