#!/usr/bin/env python3
import time
from gps import gps
from gps import WATCH_ENABLE


class GpsInterface:
    def __init__(self):
        self.data = gps(mode=WATCH_ENABLE)
        self.update()

    def update(self):
        self.data.next()


def print_gps_data(gps_interface):
    print('latitude      {}'.format(gps_interface.data.fix.latitude))
    print('longitude     {}'.format(gps_interface.data.fix.longitude))
    print('time utc      {}'.format(gps_interface.data.utc))
    print('altitude (m)  {}'.format(gps_interface.data.fix.altitude))
    print('eps           {}'.format(gps_interface.data.fix.eps))
    print('satellites    {}'.format(gps_interface.data.satellites))


if __name__ == '__main__':
    gps_interface = GpsInterface()
    print('GPS reading')
    print('-----------------------------------------')
    print_gps_data(gps_interface)

    time.sleep(5)
    gps_interface.update()
    print("\n")
    print_gps_data(gps_interface)
