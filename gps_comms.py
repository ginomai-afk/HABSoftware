# Module to initialize and parse GPS communications
import serial
import io
import pynmea2
import sys

serial_port = ""
sio = ""


def init_comms():
    global sio
    global serial_port
    serial_port = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)
    sio = io.TextIOWrapper(io.BufferedRWPair(serial_port, serial_port))
    serial_port.close()


def read_line(tries=0):
    global sio

    try:
        line = sio.readline()
    except Exception:
        if tries < sys.getrecursionlimit():
            return read_line(tries+1)
        else:
            print("Failed to read serial stream.\r\n")

    return line


def parse_GPS():
    """ Read and parse the GPS data from the serial port. """
    global serial_port
    NMEA_data = {}
    GGA_message_found = False
    RMC_message_found = False

    serial_port.open()
    while GGA_message_found is False or RMC_message_found is False:
        line = read_line()

        if GGA_message_found is False and line.find("GGA") > 0:
            GGA_message_found = True
            NMEA_message = pynmea2.parse(line)

            NMEA_data['UTC_time'] = NMEA_message.timestamp
            NMEA_data['latitude'] = NMEA_message.lat
            NMEA_data['lat_dir'] = NMEA_message.lat_dir
            NMEA_data['longitude'] = NMEA_message.lon
            NMEA_data['lon_dir'] = NMEA_message.lon_dir
            NMEA_data['altitude'] = NMEA_message.altitude
            NMEA_data['signal_quality'] = NMEA_message.gps_qual
            NMEA_data['number_of_satellites'] = NMEA_message.num_sats

        elif RMC_message_found is False and line.find("RMC") > 0:
            RMC_message_found = True
            NMEA_message = pynmea2.parse(line)

            NMEA_data['speed'] = NMEA_message.spd_over_grnd

    serial_port.close()
    return NMEA_data
