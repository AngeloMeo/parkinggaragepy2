from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import mock.GPIO as GPIO
import parking_garage
from mock.SDL_DS3231 import SDL_DS3231
from src.parking_garage import ParkingGarage
from src.parking_garage import ParkingGarageError

class TestParkingGarage(TestCase):

    @patch.object(GPIO, "setup")
    def test_detection_sensors_configuration(self, mock_setup: MagicMock):
        parking_garage = ParkingGarage()
        mock_setup.assert_any_call(ParkingGarage.INFRARED_PIN1, GPIO.IN)
        mock_setup.assert_any_call(ParkingGarage.INFRARED_PIN2, GPIO.IN)
        mock_setup.assert_any_call(ParkingGarage.INFRARED_PIN3, GPIO.IN)

    @patch.object(GPIO, "input")
    def test_check_occupancy_car_detected(self, mock_input: MagicMock):
        mock_input.return_value = False
        parking_garage = ParkingGarage()
        occupied = parking_garage.check_occupancy(parking_garage.INFRARED_PIN1)
        self.assertTrue(occupied)

    @patch.object(GPIO, "input")
    def test_check_occupancy_car_not_detected(self, mock_input: MagicMock):
        mock_input.return_value = True
        parking_garage = ParkingGarage()
        occupied = parking_garage.check_occupancy(parking_garage.INFRARED_PIN2)
        self.assertFalse(occupied)

    @patch.object(GPIO, "input")
    def test_check_occupancy_wrong_pin(self, mock_input: MagicMock):

        parking_garage = ParkingGarage()
        self.assertRaises(ParkingGarageError, parking_garage.check_occupancy, parking_garage.SERVO_PIN)