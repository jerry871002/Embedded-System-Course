import blescan

import sys

import bluetooth._bluetooth as bluez

import time
import math

# BLE
def init_ble():
    try:
        # open hci0 interface
        sock = bluez.hci_open_dev(0)
        print ("ble thread started")
    except:
        print ("error accessing bluetooth device...")
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)    # set scan params
    blescan.hci_enable_le_scan(sock)            # start scanning

    return sock

def ble_scan(sock):
    rssiDict = dict()   # create a dictionary
    returnedList = blescan.parse_events(sock)

    for beacon in returnedList:
        raw_uuid = ""
        for word in beacon.uuid.split('-'):
            raw_uuid = raw_uuid + word
        if raw_uuid == "00000000000000000000000000000000":
            print("raw_uuid", raw_uuid)
            print("uuid:", beacon.uuid)
            print("major:", beacon.major, ", minor:", beacon.minor, ", txpower:", beacon.unknown)
            print("rssi", beacon.rssi)
            print("distance", cal_distance(beacon.unknown, beacon.rssi))
            print("--------")

    return rssiDict

def cal_distance(txpower, rssi):
    txpower = float(txpower)
    rssi = float(rssi)

    if rssi == 0:
        return -1

    ratio = rssi / txpower
    if ratio < 1:
        return math.pow(ratio, 10)
    else:
        return 0.42093 * math.pow(ratio, 6.9476) + 0.54992

def main():

    sock = init_ble()

    while True:
        rssiDict = ble_scan(sock)


if __name__ == "__main__":
    main()
