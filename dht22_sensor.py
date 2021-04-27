#!/usr/bin/env python3
"""
File Name: dht22_sensor.py
Python Version: 3.7
Date Created: 04/27/2021

Create and poll and DHT22 sensor device.
"""

import os
import board
import adafruit_dht
from threading import Thread
import time

__author__ = "Mathew Henderson"
__copyright__ = "Copyright (C) 2021"
__license__ = "GPL-3.0"
__version__ = "0.0.1"


class Dht22Sensor(Thread):
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
        Thread.__init__(self)
        self.temperature_c = None
        self.humidity = None
        self.running = True
        self._sensor = adafruit_dht.DHT22(board.D17, use_pulseio=False)
        self._current_temperature_reading = None
        self._current_humidity_reading = None

    def run(self):
        """
        This thread reads the temperature and humidity of the DHT22 sensor
        every 2 seconds.  If the readings are valid, it updates the
        'temperature_c' and 'humidity' attributes.
        """
        while self.running:
            # The minimum time required by the DHT22
            # is 2 seconds between reads.
            time.sleep(2.0)

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
    sensor = Dht22Sensor()

    try:
        sensor.start()

        while True:
            os.system('clear')

            print("Temperature     Humidity")
            print("------------------------")
            print("   {0}            {1}".format(sensor.temperature_c,
                                                 sensor.humidity))
            time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        sensor.running = False
        sensor.join()

    print("Done.\nExiting.")
