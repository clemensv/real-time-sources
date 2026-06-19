"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.station import Station
from noaa_producer_data.microsoft.opendata.us.noaa.unnamedclass import UnnamedClass


class Test_Station(unittest.TestCase):
    """
    Test case for Station
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_Station.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of Station for testing
        """
        instance = Station(
            tidal=True,
            greatlakes=False,
            shefcode='shwlfgzwfgdvjqdqanyg',
            details=None,
            sensors=None,
            floodlevels=None,
            datums=None,
            supersededdatums=None,
            harmonicConstituents=None,
            benchmarks=None,
            tidePredOffsets=None,
            ofsMapOffsets=None,
            state='yxfszrijosmrythfjnqv',
            timezone='qfcppazztpewbuifklyx',
            timezonecorr=int(55),
            observedst=False,
            stormsurge=False,
            nearby=None,
            forecast=False,
            outlook=False,
            HTFhistorical=False,
            nonNavigational=True,
            station_id='cpybbpnnimfbtjnduhwr',
            name='clazeberokxilbdzqeyh',
            lat=float(83.25474036054396),
            lng=float(73.74979555755053),
            affiliations='wrnuvbgqomgxkjqeofcn',
            portscode='ycigkeenbmihqxbnajjn',
            products=None,
            disclaimers=None,
            notices=None,
            self_='gxvatfxuatkkevgpnbbs',
            expand='vvcmxzthmelfiygapuiy',
            tideType='cbyquvlxcoanszmlqsgl'
        )
        return instance

    
    def test_tidal_property(self):
        """
        Test tidal property
        """
        test_value = True
        self.instance.tidal = test_value
        self.assertEqual(self.instance.tidal, test_value)
    
    def test_greatlakes_property(self):
        """
        Test greatlakes property
        """
        test_value = False
        self.instance.greatlakes = test_value
        self.assertEqual(self.instance.greatlakes, test_value)
    
    def test_shefcode_property(self):
        """
        Test shefcode property
        """
        test_value = 'shwlfgzwfgdvjqdqanyg'
        self.instance.shefcode = test_value
        self.assertEqual(self.instance.shefcode, test_value)
    
    def test_details_property(self):
        """
        Test details property
        """
        test_value = None
        self.instance.details = test_value
        self.assertEqual(self.instance.details, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = None
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_floodlevels_property(self):
        """
        Test floodlevels property
        """
        test_value = None
        self.instance.floodlevels = test_value
        self.assertEqual(self.instance.floodlevels, test_value)
    
    def test_datums_property(self):
        """
        Test datums property
        """
        test_value = None
        self.instance.datums = test_value
        self.assertEqual(self.instance.datums, test_value)
    
    def test_supersededdatums_property(self):
        """
        Test supersededdatums property
        """
        test_value = None
        self.instance.supersededdatums = test_value
        self.assertEqual(self.instance.supersededdatums, test_value)
    
    def test_harmonicConstituents_property(self):
        """
        Test harmonicConstituents property
        """
        test_value = None
        self.instance.harmonicConstituents = test_value
        self.assertEqual(self.instance.harmonicConstituents, test_value)
    
    def test_benchmarks_property(self):
        """
        Test benchmarks property
        """
        test_value = None
        self.instance.benchmarks = test_value
        self.assertEqual(self.instance.benchmarks, test_value)
    
    def test_tidePredOffsets_property(self):
        """
        Test tidePredOffsets property
        """
        test_value = None
        self.instance.tidePredOffsets = test_value
        self.assertEqual(self.instance.tidePredOffsets, test_value)
    
    def test_ofsMapOffsets_property(self):
        """
        Test ofsMapOffsets property
        """
        test_value = None
        self.instance.ofsMapOffsets = test_value
        self.assertEqual(self.instance.ofsMapOffsets, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'yxfszrijosmrythfjnqv'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'qfcppazztpewbuifklyx'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_timezonecorr_property(self):
        """
        Test timezonecorr property
        """
        test_value = int(55)
        self.instance.timezonecorr = test_value
        self.assertEqual(self.instance.timezonecorr, test_value)
    
    def test_observedst_property(self):
        """
        Test observedst property
        """
        test_value = False
        self.instance.observedst = test_value
        self.assertEqual(self.instance.observedst, test_value)
    
    def test_stormsurge_property(self):
        """
        Test stormsurge property
        """
        test_value = False
        self.instance.stormsurge = test_value
        self.assertEqual(self.instance.stormsurge, test_value)
    
    def test_nearby_property(self):
        """
        Test nearby property
        """
        test_value = None
        self.instance.nearby = test_value
        self.assertEqual(self.instance.nearby, test_value)
    
    def test_forecast_property(self):
        """
        Test forecast property
        """
        test_value = False
        self.instance.forecast = test_value
        self.assertEqual(self.instance.forecast, test_value)
    
    def test_outlook_property(self):
        """
        Test outlook property
        """
        test_value = False
        self.instance.outlook = test_value
        self.assertEqual(self.instance.outlook, test_value)
    
    def test_HTFhistorical_property(self):
        """
        Test HTFhistorical property
        """
        test_value = False
        self.instance.HTFhistorical = test_value
        self.assertEqual(self.instance.HTFhistorical, test_value)
    
    def test_nonNavigational_property(self):
        """
        Test nonNavigational property
        """
        test_value = True
        self.instance.nonNavigational = test_value
        self.assertEqual(self.instance.nonNavigational, test_value)
    
    def test_station_id_property(self):
        """
        Test station_id property
        """
        test_value = 'cpybbpnnimfbtjnduhwr'
        self.instance.station_id = test_value
        self.assertEqual(self.instance.station_id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'clazeberokxilbdzqeyh'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(83.25474036054396)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lng_property(self):
        """
        Test lng property
        """
        test_value = float(73.74979555755053)
        self.instance.lng = test_value
        self.assertEqual(self.instance.lng, test_value)
    
    def test_affiliations_property(self):
        """
        Test affiliations property
        """
        test_value = 'wrnuvbgqomgxkjqeofcn'
        self.instance.affiliations = test_value
        self.assertEqual(self.instance.affiliations, test_value)
    
    def test_portscode_property(self):
        """
        Test portscode property
        """
        test_value = 'ycigkeenbmihqxbnajjn'
        self.instance.portscode = test_value
        self.assertEqual(self.instance.portscode, test_value)
    
    def test_products_property(self):
        """
        Test products property
        """
        test_value = None
        self.instance.products = test_value
        self.assertEqual(self.instance.products, test_value)
    
    def test_disclaimers_property(self):
        """
        Test disclaimers property
        """
        test_value = None
        self.instance.disclaimers = test_value
        self.assertEqual(self.instance.disclaimers, test_value)
    
    def test_notices_property(self):
        """
        Test notices property
        """
        test_value = None
        self.instance.notices = test_value
        self.assertEqual(self.instance.notices, test_value)
    
    def test_self__property(self):
        """
        Test self_ property
        """
        test_value = 'gxvatfxuatkkevgpnbbs'
        self.instance.self_ = test_value
        self.assertEqual(self.instance.self_, test_value)
    
    def test_expand_property(self):
        """
        Test expand property
        """
        test_value = 'vvcmxzthmelfiygapuiy'
        self.instance.expand = test_value
        self.assertEqual(self.instance.expand, test_value)
    
    def test_tideType_property(self):
        """
        Test tideType property
        """
        test_value = 'cbyquvlxcoanszmlqsgl'
        self.instance.tideType = test_value
        self.assertEqual(self.instance.tideType, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = Station.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

