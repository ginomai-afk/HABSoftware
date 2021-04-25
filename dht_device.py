#!/usr/bin/env python3
"""
File Name: dht_device.py
Python Version: 3.7
Date Created: 04/10/2021

Create and poll and DHT22 sensor device.
"""

from time import time
import board
import adafruit_dht

__author__ = "Mathew Henderson"
__copyright__ = "Copyright (C) 2021"
__license__ = "GPL-3.0"
__version__ = "0.0.1"


class DhtDevice:
    """
    Class used to initialize and get readings from a DHT22 temperature
    and humidity sensor.

    Attributes
    ----------
    temperature_c : float
        The temperature reading in degrees Celsius
    humidity : float
        The humidity reading as a measure of relative humidity
    _sensor : DHT22 class
        DHT22 sensor class from adafruit_dht library
    _previous_time: float
        The time() reading taken from the previous polling of the sensor
    _current_temperature_reading: float
        Temperature reading from the DHT22 sensor
    _current_humidity_reading: float
        Humidity reading from the DHT22 sensor

    Methods
    -------
    poll_sensor()
        Check the DHT22 sensor and update 'temperature_c' and
        'humidity' attributes with most recent valid readings.
    """

    def __init__(self):
        """Initialize the DHT22 sensor attributes."""

        self.temperature_c = None
        self.humidity = None
        self._sensor = adafruit_dht.DHT22(board.D17)
        self._previous_time = time()
        self._current_temperature_reading = None
        self._current_humidity_reading = None

    def poll_sensor(self, elapsed_time_s=2.0):
        """
        Read the temperature and humidity of the DHT22 sensor every
        'elapsed_time_s'.  If the readings are valid, updates the
        'temperature_c' and 'humidity' attributes. Note that 'elapsed_time_s'
        must be a minimum of 2.0 seconds.

        Parameters
        ----------
        elapsed_time_s : float, optional
            Number of seconds between sensor readings (default is 2.0)

        Raises
        ------
        AssertionError
            If 'elapsed_time_s' is less than 2.0
        """
        assert (elapsed_time_s >= 2.0), "elapsed_time_s must be >= 2.0"

        if ((time() - self._previous_time) >= elapsed_time_s):
            self._previous_time = time()
            try:
                self._current_temperature_reading = self._sensor.temperature
                self._current_humidity_reading = self._sensor.humidity

            except RuntimeError:
                self._current_temperature_reading = None
                self._current_humidity_reading = None

            if (self._current_temperature_reading is not None and
                    self._current_humidity_reading is not None):
                self.temperature_c = self._current_temperature_reading
                self.humidity = self._current_humidity_reading


if __name__ == '__main__':
    sensor = DhtDevice()

    while True:
        temperature_last_reading = None
        humidity_last_reading = None

        sensor.poll_sensor()

        if (temperature_last_reading != sensor.temperature_c or
                humidity_last_reading != sensor.humidity):
            temperature_last_reading = sensor.temperature_c
            humidity_last_reading = sensor.humidity

            print("{}C, {}%\n".format(temperature_last_reading,
                                      humidity_last_reading))
