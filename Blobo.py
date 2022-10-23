#!/usr/bin/env python

"""
Blobo game controller driver, with pybluez.
"""

import bluetooth
import time
import struct
from threading import Thread

class Blobo:
    BT_SERIAL_PORT = "00001101-0000-1000-8000-00805F9B34FB"

    @classmethod
    def find_all(self, duration = 5):
        nearby_devices = bluetooth.discover_devices(duration = duration, lookup_names = True, flush_cache = True, lookup_class = False)
        nearby_blobos = [address for address, name in nearby_devices if "BALL" in name and self.find_service(address)]
        return nearby_blobos

    @classmethod
    def find_service(self, address):
        services = bluetooth.find_service(address = address, uuid = self.BT_SERIAL_PORT)
        if services:
            return services[0]

    def __init__(self, address):
        self.stopped = False
        self.accelerometer = self.gyroscope = self.magnetometer = (0, 0, 0)
        self.pressure = 0

        service = self.find_service(address)
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.socket.connect((service["host"], service["port"]))
        self.thread = Thread(target = self.run)
        self.thread.start()

    def parse(self, data):
        packet = struct.unpack("4B10hB", data)
        if packet[0] == 0 and packet[1] == 65:
            self.accelerometer = packet[4:7]
            self.gyroscope = packet[7:10]
            self.pressure = packet[10]
            self.magnetometer = packet[11:14]
        else:
            pass # raise RuntimeError("Unknown Blobo packet.")

    def run(self):
        try:
            time_keepalive = time.time()
            self.socket.send(b"A")
            data = bytearray()
            while not self.stopped:
                time_now = time.time()
                if len(data) == 25:
                    packet = data
                    data = bytearray()
                    self.parse(packet)
                    self.time = time_now
                if time_now > time_keepalive:
                    time_keepalive += 0.1
                    self.socket.send(b"\r")
                data.extend(self.socket.recv(25 - len(data)))
        finally:
            self.socket.close()
            self.stopped = True

    def stop(self):
        self.stopped = True
        if self.thread:
            self.thread.join()
            self.thread = None
