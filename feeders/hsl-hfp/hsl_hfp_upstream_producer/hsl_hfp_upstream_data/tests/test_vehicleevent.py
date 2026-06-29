"""
Test case for VehicleEvent
"""

import os
import sys
import unittest

sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), '../src'.replace('/', os.sep))))

from hsl_hfp_upstream_data.fi.hsl.hfp.vehicleevent import VehicleEvent
from typing import Any


class Test_VehicleEvent(unittest.TestCase):
    """
    Test case for VehicleEvent
    """

    def setUp(self):
        """
        Set up test case
        """
        self.instance = Test_VehicleEvent.create_instance()

    @staticmethod
    def create_instance():
        """
        Create instance of VehicleEvent for testing
        """
        instance = VehicleEvent(
            oper=int(50),
            veh=int(74),
            tst='itkvjrgcnthmgzrkzlcx',
            tsi=int(75),
            operator_id='urxgkxqpnadxwsfqbkjp',
            vehicle_number='vszbgzyowigvorcdlxba',
            temporal_type=None,
            transport_mode=None,
            route_id='lheoyvqlgeqnrlngnqkh',
            direction_id='llzikxxheutusjtebfmu',
            headsign='saoljrydixyrgffpgpnl',
            start_time='fbapiwqwekpmjhlvddjs',
            next_stop='fawtksmeuwmxgonazakg',
            geohash_level='jmkccdroxiaanbcorfsq',
            geohash='kleuoplvyhbsglazwjgq',
            desi='pjcvwofnehyrftwzfaxy',
            dir='roohpapyaihiwliwxuzr',
            dl=int(61),
            oday='evwvlrigkovfhefawvzv',
            jrn=int(92),
            line=int(80),
            start='huonzmkucwtuszpwsoyx',
            stop=int(33),
            route='rscbkeeznjuaebbjdoxu',
            occu=int(68),
            seq=int(45),
            label='bzkwfpjxfwdqjabnmgcf',
            spd=float(41.75429008609826),
            hdg=int(71),
            lat=float(80.74093905402421),
            long=float(19.685298914832728),
            acc=float(91.80676181448422),
            odo=int(46),
            drst=int(44),
            loc='weogrbxsbpioriuqydvd',
            ttarr='ujvajrzqlxkouapqjreu',
            ttdep='knotdlrysfbvnqtvydyj',
            dr_type=int(64)
        )
        return instance

    
    def test_oper_property(self):
        """
        Test oper property
        """
        test_value = int(50)
        self.instance.oper = test_value
        self.assertEqual(self.instance.oper, test_value)
    
    def test_veh_property(self):
        """
        Test veh property
        """
        test_value = int(74)
        self.instance.veh = test_value
        self.assertEqual(self.instance.veh, test_value)
    
    def test_tst_property(self):
        """
        Test tst property
        """
        test_value = 'itkvjrgcnthmgzrkzlcx'
        self.instance.tst = test_value
        self.assertEqual(self.instance.tst, test_value)
    
    def test_tsi_property(self):
        """
        Test tsi property
        """
        test_value = int(75)
        self.instance.tsi = test_value
        self.assertEqual(self.instance.tsi, test_value)
    
    def test_operator_id_property(self):
        """
        Test operator_id property
        """
        test_value = 'urxgkxqpnadxwsfqbkjp'
        self.instance.operator_id = test_value
        self.assertEqual(self.instance.operator_id, test_value)
    
    def test_vehicle_number_property(self):
        """
        Test vehicle_number property
        """
        test_value = 'vszbgzyowigvorcdlxba'
        self.instance.vehicle_number = test_value
        self.assertEqual(self.instance.vehicle_number, test_value)
    
    def test_temporal_type_property(self):
        """
        Test temporal_type property
        """
        test_value = None
        self.instance.temporal_type = test_value
        self.assertEqual(self.instance.temporal_type, test_value)
    
    def test_transport_mode_property(self):
        """
        Test transport_mode property
        """
        test_value = None
        self.instance.transport_mode = test_value
        self.assertEqual(self.instance.transport_mode, test_value)
    
    def test_route_id_property(self):
        """
        Test route_id property
        """
        test_value = 'lheoyvqlgeqnrlngnqkh'
        self.instance.route_id = test_value
        self.assertEqual(self.instance.route_id, test_value)
    
    def test_direction_id_property(self):
        """
        Test direction_id property
        """
        test_value = 'llzikxxheutusjtebfmu'
        self.instance.direction_id = test_value
        self.assertEqual(self.instance.direction_id, test_value)
    
    def test_headsign_property(self):
        """
        Test headsign property
        """
        test_value = 'saoljrydixyrgffpgpnl'
        self.instance.headsign = test_value
        self.assertEqual(self.instance.headsign, test_value)
    
    def test_start_time_property(self):
        """
        Test start_time property
        """
        test_value = 'fbapiwqwekpmjhlvddjs'
        self.instance.start_time = test_value
        self.assertEqual(self.instance.start_time, test_value)
    
    def test_next_stop_property(self):
        """
        Test next_stop property
        """
        test_value = 'fawtksmeuwmxgonazakg'
        self.instance.next_stop = test_value
        self.assertEqual(self.instance.next_stop, test_value)
    
    def test_geohash_level_property(self):
        """
        Test geohash_level property
        """
        test_value = 'jmkccdroxiaanbcorfsq'
        self.instance.geohash_level = test_value
        self.assertEqual(self.instance.geohash_level, test_value)
    
    def test_geohash_property(self):
        """
        Test geohash property
        """
        test_value = 'kleuoplvyhbsglazwjgq'
        self.instance.geohash = test_value
        self.assertEqual(self.instance.geohash, test_value)
    
    def test_desi_property(self):
        """
        Test desi property
        """
        test_value = 'pjcvwofnehyrftwzfaxy'
        self.instance.desi = test_value
        self.assertEqual(self.instance.desi, test_value)
    
    def test_dir_property(self):
        """
        Test dir property
        """
        test_value = 'roohpapyaihiwliwxuzr'
        self.instance.dir = test_value
        self.assertEqual(self.instance.dir, test_value)
    
    def test_dl_property(self):
        """
        Test dl property
        """
        test_value = int(61)
        self.instance.dl = test_value
        self.assertEqual(self.instance.dl, test_value)
    
    def test_oday_property(self):
        """
        Test oday property
        """
        test_value = 'evwvlrigkovfhefawvzv'
        self.instance.oday = test_value
        self.assertEqual(self.instance.oday, test_value)
    
    def test_jrn_property(self):
        """
        Test jrn property
        """
        test_value = int(92)
        self.instance.jrn = test_value
        self.assertEqual(self.instance.jrn, test_value)
    
    def test_line_property(self):
        """
        Test line property
        """
        test_value = int(80)
        self.instance.line = test_value
        self.assertEqual(self.instance.line, test_value)
    
    def test_start_property(self):
        """
        Test start property
        """
        test_value = 'huonzmkucwtuszpwsoyx'
        self.instance.start = test_value
        self.assertEqual(self.instance.start, test_value)
    
    def test_stop_property(self):
        """
        Test stop property
        """
        test_value = int(33)
        self.instance.stop = test_value
        self.assertEqual(self.instance.stop, test_value)
    
    def test_route_property(self):
        """
        Test route property
        """
        test_value = 'rscbkeeznjuaebbjdoxu'
        self.instance.route = test_value
        self.assertEqual(self.instance.route, test_value)
    
    def test_occu_property(self):
        """
        Test occu property
        """
        test_value = int(68)
        self.instance.occu = test_value
        self.assertEqual(self.instance.occu, test_value)
    
    def test_seq_property(self):
        """
        Test seq property
        """
        test_value = int(45)
        self.instance.seq = test_value
        self.assertEqual(self.instance.seq, test_value)
    
    def test_label_property(self):
        """
        Test label property
        """
        test_value = 'bzkwfpjxfwdqjabnmgcf'
        self.instance.label = test_value
        self.assertEqual(self.instance.label, test_value)
    
    def test_spd_property(self):
        """
        Test spd property
        """
        test_value = float(41.75429008609826)
        self.instance.spd = test_value
        self.assertEqual(self.instance.spd, test_value)
    
    def test_hdg_property(self):
        """
        Test hdg property
        """
        test_value = int(71)
        self.instance.hdg = test_value
        self.assertEqual(self.instance.hdg, test_value)
    
    def test_lat_property(self):
        """
        Test lat property
        """
        test_value = float(80.74093905402421)
        self.instance.lat = test_value
        self.assertEqual(self.instance.lat, test_value)
    
    def test_long_property(self):
        """
        Test long property
        """
        test_value = float(19.685298914832728)
        self.instance.long = test_value
        self.assertEqual(self.instance.long, test_value)
    
    def test_acc_property(self):
        """
        Test acc property
        """
        test_value = float(91.80676181448422)
        self.instance.acc = test_value
        self.assertEqual(self.instance.acc, test_value)
    
    def test_odo_property(self):
        """
        Test odo property
        """
        test_value = int(46)
        self.instance.odo = test_value
        self.assertEqual(self.instance.odo, test_value)
    
    def test_drst_property(self):
        """
        Test drst property
        """
        test_value = int(44)
        self.instance.drst = test_value
        self.assertEqual(self.instance.drst, test_value)
    
    def test_loc_property(self):
        """
        Test loc property
        """
        test_value = 'weogrbxsbpioriuqydvd'
        self.instance.loc = test_value
        self.assertEqual(self.instance.loc, test_value)
    
    def test_ttarr_property(self):
        """
        Test ttarr property
        """
        test_value = 'ujvajrzqlxkouapqjreu'
        self.instance.ttarr = test_value
        self.assertEqual(self.instance.ttarr, test_value)
    
    def test_ttdep_property(self):
        """
        Test ttdep property
        """
        test_value = 'knotdlrysfbvnqtvydyj'
        self.instance.ttdep = test_value
        self.assertEqual(self.instance.ttdep, test_value)
    
    def test_dr_type_property(self):
        """
        Test dr_type property
        """
        test_value = int(64)
        self.instance.dr_type = test_value
        self.assertEqual(self.instance.dr_type, test_value)
    
    def test_to_byte_array_json(self):
        """
        Test to_byte_array method with json media type
        """
        media_type = "application/json"
        bytes_data = self.instance.to_byte_array(media_type)
        new_instance = VehicleEvent.from_data(bytes_data, media_type)
        bytes_data2 = new_instance.to_byte_array(media_type)
        self.assertEqual(bytes_data, bytes_data2)

    def test_to_json(self):
        """
        Test to_json method
        """
        json_data = self.instance.to_json()
        new_instance = VehicleEvent.from_json(json_data)
        json_data2 = new_instance.to_json()
        self.assertEqual(json_data, json_data2)

