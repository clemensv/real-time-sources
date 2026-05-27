"""Unit test: --once flag causes poll_and_send to exit after one cycle."""

from unittest.mock import MagicMock, patch

from noaa_goes.noaa_goes import SWPCPoller


def _build_poller():
    with patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCAlertsEventProducer'), \
         patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCObservationsEventProducer'), \
         patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCGOESParticleFluxEventProducer'), \
         patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCGOESMagnetometerEventProducer'), \
         patch('noaa_goes.noaa_goes.MicrosoftOpenDataUSNOAASWPCSolarFlaresEventProducer'), \
         patch('confluent_kafka.Producer'):
        poller = SWPCPoller(
            kafka_config={'bootstrap.servers': 'localhost:9092'},
            kafka_topic='test',
            last_polled_file='/tmp/test_state.json',
        )
    poller.kafka_producer = MagicMock()
    for attr in ('alerts_producer', 'observations_producer',
                 'particle_flux_producer', 'magnetometer_producer',
                 'flares_producer'):
        setattr(poller, attr, MagicMock())
    return poller


def test_once_mode_exits_after_single_cycle():
    poller = _build_poller()
    poller.load_state = MagicMock(return_value={})
    poller.save_state = MagicMock()
    for name in ('_send_alerts', '_send_k_index', '_send_solar_wind_summary',
                 '_send_plasma', '_send_mag', '_send_goes_xrays',
                 '_send_goes_protons', '_send_goes_electrons',
                 '_send_goes_magnetometers', '_send_xray_flares'):
        setattr(poller, name, MagicMock(return_value=0))

    with patch('noaa_goes.noaa_goes.time.sleep') as mock_sleep:
        poller.poll_and_send(once=True)
        mock_sleep.assert_not_called()

    poller.load_state.assert_called_once()
    poller.save_state.assert_called_once()
    poller._send_alerts.assert_called_once()


def test_default_mode_does_not_exit_after_single_cycle():
    """Without once=True, the loop calls time.sleep between cycles."""
    poller = _build_poller()
    poller.load_state = MagicMock(return_value={})
    poller.save_state = MagicMock()
    for name in ('_send_alerts', '_send_k_index', '_send_solar_wind_summary',
                 '_send_plasma', '_send_mag', '_send_goes_xrays',
                 '_send_goes_protons', '_send_goes_electrons',
                 '_send_goes_magnetometers', '_send_xray_flares'):
        setattr(poller, name, MagicMock(return_value=0))

    # Make the second sleep break out so the test terminates.
    call_count = {'n': 0}

    def fake_sleep(_seconds):
        call_count['n'] += 1
        raise KeyboardInterrupt()

    with patch('noaa_goes.noaa_goes.time.sleep', side_effect=fake_sleep):
        try:
            poller.poll_and_send(once=False)
        except KeyboardInterrupt:
            pass

    assert call_count['n'] == 1
