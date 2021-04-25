#!/usr/bin/env python3
"""
File Name: main.py
Python Version: 3.7
Date Created: 04/04/2021

This code was created for use with the Raspberry Pi module.  It utilizes a
Pi Camera, DHT22 sensor, BMP388 sensor and a custom daughter board with a uBlox
GPS receiver.  Using this hardware, it logs data collected from each sensor.
"""

import gps_polling
import time
from picamera import PiCamera
from dht_device import DhtDevice
import board
import busio
import adafruit_bmp3xx

__author__ = "Mathew Henderson"
__copyright__ = "Copyright (C) 2021"
__license__ = "GPL-3.0"
__version__ = "0.0.1"


def take_picture(camera, file_name):
    camera.start_preview()
    time.sleep(5)
    camera.capture('/home/pi/HABSoftware/photos/%s' % file_name)
    camera.stop_preview()


def init_camera():
    camera = PiCamera()
    camera.led = False
    camera.resolution = (1024, 768)
    camera.rotation = 180
    return camera


if __name__ == '__main__':
    gps_data = gps_polling.GpsPoller()
    camera = init_camera()
    iteration = 0
    dht_sensor = DhtDevice()
    i2c = busio.I2C(board.SCL, board.SDA)
    bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
    bmp.sea_level_pressure = 1023.5
    current_time = time.time()

    try:
        # Start a thread to the gps daemon.
        gps_data.start()

        print("Iteration,Status,NumSats,Time,Lat,Long,Alt,"
              "Speed,Temp,Humidity,Pressure,Temp,Alt")
        while True:
            dht_sensor.poll_sensor()

            if ((time.time() - current_time) >= 30):
                current_time = time.time()
                print("{},{},{},{},{},{},{},{},{},{},{:.2f},{:.2f},{:.2f}".format(
                    str(iteration),
                    str(gps_data.gpsd.fix.mode),
                    str(gps_data.gpsd.satellites_used),
                    gps_data.gpsd.fix.time,
                    gps_data.gpsd.fix.latitude,
                    gps_data.gpsd.fix.longitude,
                    gps_data.gpsd.fix.altitude,
                    gps_data.gpsd.fix.speed,
                    dht_sensor.temperature_c,
                    dht_sensor.humidity,
                    bmp.pressure,
                    bmp.temperature,
                    bmp.altitude))
                take_picture(camera, ("{}.jpg".format(str(iteration))))
                iteration += 1

    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        gps_data.running = False
        gps_data.join()

    print("Done.\nExiting.")
