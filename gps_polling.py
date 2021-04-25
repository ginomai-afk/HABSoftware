import os
import time
import threading

from gps import gps
from gps import WATCH_ENABLE


os.system('clear')


class GpsPoller(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def run(self):
        while self.running:
            self.gpsd.next()
            time.sleep(0.5)


if __name__ == '__main__':
    poll_gps = GpsPoller()
    try:
        poll_gps.start()

        while True:
            os.system('clear')

            print('GPS reading')
            print('-----------------------------------------')
            print('latitude      {}'.format(poll_gps.gpsd.fix.latitude))
            print('longitude     {}'.format(poll_gps.gpsd.fix.longitude))
            print('time utc      {}'.format(poll_gps.gpsd.utc))
            print('altitude (m)  {}'.format(poll_gps.gpsd.fix.altitude))
            print('eps           {}'.format(poll_gps.gpsd.fix.eps))
            print('satellites    {}'.format(poll_gps.gpsd.satellites))

            time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        poll_gps.running = False
        poll_gps.join()

    print("Done.\nExiting.")
