"""
Test case for Station
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from noaa_producer_data.microsoft.opendata.us.noaa.station import Station
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_benchmarks import Test_Benchmarks
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_supersededdatums import Test_Supersededdatums
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_ofsmapoffsets import Test_OfsMapOffsets
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_disclaimers import Test_Disclaimers
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_datums import Test_Datums
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_sensors import Test_Sensors
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_harmonicconstituents import Test_HarmonicConstituents
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_tidepredoffsets import Test_TidePredOffsets
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_floodlevels import Test_Floodlevels
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_notices import Test_Notices
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_nearby import Test_Nearby
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_products import Test_Products
from test_noaa_producer_data_microsoft_opendata_us_noaa_stationtypes_details import Test_Details


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
            greatlakes=True,
            shefcode='sakcwzvhctvfvroqnvsa',
            details=Test_Details.create_instance(),
            sensors=Test_Sensors.create_instance(),
            floodlevels=Test_Floodlevels.create_instance(),
            datums=Test_Datums.create_instance(),
            supersededdatums=Test_Supersededdatums.create_instance(),
            harmonicConstituents=Test_HarmonicConstituents.create_instance(),
            benchmarks=Test_Benchmarks.create_instance(),
            tidePredOffsets=Test_TidePredOffsets.create_instance(),
            ofsMapOffsets=Test_OfsMapOffsets.create_instance(),
            state='dbnutpzhakrscrirszac',
            timezone='golkojfsvafmpubiixrh',
            timezonecorr=int(75),
            observedst=True,
            stormsurge=False,
            nearby=Test_Nearby.create_instance(),
            forecast=True,
            outlook=False,
            HTFhistorical=False,
            nonNavigational=True,
            id='esihrezfyrpdocdirvkw',
            name='fwodcnumyrqokfnpailh',
            lat=float(17.09812477750917),
            lng=float(1.889629918308755),
            affiliations='kvkzpaaxudvctnclrjwx',
            portscode='dftvvlapbnutyqmvevqx',
            products=Test_Products.create_instance(),
            disclaimers=Test_Disclaimers.create_instance(),
            notices=Test_Notices.create_instance(),
            self_='snanaqwqbvkgyhumeubo',
            expand='lbzdqnwbngudgbsgvurt',
            tideType='rqfrywgiateaartfmwsx'
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
        test_value = True
        self.instance.greatlakes = test_value
        self.assertEqual(self.instance.greatlakes, test_value)
    
    def test_shefcode_property(self):
        """
        Test shefcode property
        """
        test_value = 'sakcwzvhctvfvroqnvsa'
        self.instance.shefcode = test_value
        self.assertEqual(self.instance.shefcode, test_value)
    
    def test_details_property(self):
        """
        Test details property
        """
        test_value = Test_Details.create_instance()
        self.instance.details = test_value
        self.assertEqual(self.instance.details, test_value)
    
    def test_sensors_property(self):
        """
        Test sensors property
        """
        test_value = Test_Sensors.create_instance()
        self.instance.sensors = test_value
        self.assertEqual(self.instance.sensors, test_value)
    
    def test_floodlevels_property(self):
        """
        Test floodlevels property
        """
        test_value = Test_Floodlevels.create_instance()
        self.instance.floodlevels = test_value
        self.assertEqual(self.instance.floodlevels, test_value)
    
    def test_datums_property(self):
        """
        Test datums property
        """
        test_value = Test_Datums.create_instance()
        self.instance.datums = test_value
        self.assertEqual(self.instance.datums, test_value)
    
    def test_supersededdatums_property(self):
        """
        Test supersededdatums property
        """
        test_value = Test_Supersededdatums.create_instance()
        self.instance.supersededdatums = test_value
        self.assertEqual(self.instance.supersededdatums, test_value)
    
    def test_harmonicConstituents_property(self):
        """
        Test harmonicConstituents property
        """
        test_value = Test_HarmonicConstituents.create_instance()
        self.instance.harmonicConstituents = test_value
        self.assertEqual(self.instance.harmonicConstituents, test_value)
    
    def test_benchmarks_property(self):
        """
        Test benchmarks property
        """
        test_value = Test_Benchmarks.create_instance()
        self.instance.benchmarks = test_value
        self.assertEqual(self.instance.benchmarks, test_value)
    
    def test_tidePredOffsets_property(self):
        """
        Test tidePredOffsets property
        """
        test_value = Test_TidePredOffsets.create_instance()
        self.instance.tidePredOffsets = test_value
        self.assertEqual(self.instance.tidePredOffsets, test_value)
    
    def test_ofsMapOffsets_property(self):
        """
        Test ofsMapOffsets property
        """
        test_value = Test_OfsMapOffsets.create_instance()
        self.instance.ofsMapOffsets = test_value
        self.assertEqual(self.instance.ofsMapOffsets, test_value)
    
    def test_state_property(self):
        """
        Test state property
        """
        test_value = 'dbnutpzhakrscrirszac'
        self.instance.state = test_value
        self.assertEqual(self.instance.state, test_value)
    
    def test_timezone_property(self):
        """
        Test timezone property
        """
        test_value = 'golkojfsvafmpubiixrh'
        self.instance.timezone = test_value
        self.assertEqual(self.instance.timezone, test_value)
    
    def test_timezonecorr_property(self):
        """
        Test timezonecorr property
        """
        test_value = int(75)
        self.instance.timezonecorr = test_value
        self.assertEqual(self.instance.timezonecorr, test_value)
    
    def test_observedst_property(self):
        """
        Test observedst property
        """
        test_value = True
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
        test_value = Test_Nearby.create_instance()
        self.instance.nearby = test_value
        self.assertEqual(self.instance.nearby, test_value)
    
    def test_forecast_property(self):
        """
        Test forecast property
        """
        test_value = True
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
    
    def test_id_property(self):
        """
        Test id property
        """
        test_value = 'esihrezfyrpdocdirvkw'
        self.instance.id = test_value
        self.assertEqual(self.instance.id, test_value)
    
    def test_name_property(self):
        """
        Test name property
        """
        test_value = 'fwodcnumyrqokfnpailh'
        self.instance.name = test_value
        self.assertEqual(self.instance.name, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(17.09812477750917)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_lng_property(self):
        """
        Test lng property
        """
        test_value = float(1.889629918308755)
        self.instance.lng = test_value
        self.assertEqual(self.instance.lng, test_value)
    
    def test_affiliations_property(self):
        """
        Test affiliations property
        """
        test_value = 'kvkzpaaxudvctnclrjwx'
        self.instance.affiliations = test_value
        self.assertEqual(self.instance.affiliations, test_value)
    
    def test_portscode_property(self):
        """
        Test portscode property
        """
        test_value = 'dftvvlapbnutyqmvevqx'
        self.instance.portscode = test_value
        self.assertEqual(self.instance.portscode, test_value)
    
    def test_products_property(self):
        """
        Test products property
        """
        test_value = Test_Products.create_instance()
        self.instance.products = test_value
        self.assertEqual(self.instance.products, test_value)
    
    def test_disclaimers_property(self):
        """
        Test disclaimers property
        """
        test_value = Test_Disclaimers.create_instance()
        self.instance.disclaimers = test_value
        self.assertEqual(self.instance.disclaimers, test_value)
    
    def test_notices_property(self):
        """
        Test notices property
        """
        test_value = Test_Notices.create_instance()
        self.instance.notices = test_value
        self.assertEqual(self.instance.notices, test_value)
    
    def test_self__property(self):
        """
        Test self_ property
        """
        test_value = 'snanaqwqbvkgyhumeubo'
        self.instance.self_ = test_value
        self.assertEqual(self.instance.self_, test_value)
    
    def test_expand_property(self):
        """
        Test expand property
        """
        test_value = 'lbzdqnwbngudgbsgvurt'
        self.instance.expand = test_value
        self.assertEqual(self.instance.expand, test_value)
    
    def test_tideType_property(self):
        """
        Test tideType property
        """
        test_value = 'rqfrywgiateaartfmwsx'
        self.instance.tideType = test_value
        self.assertEqual(self.instance.tideType, test_value)
    
    def test_to_byte_array_avro(self):
        """
        Test to_byte_array method with avro media type
        """
        media_type = "application/vnd.apache.avro+avro"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = Station.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)
