#!/usr/bin/env python3
import serial
import logging

class MH_Z19:

    __GET = b"\xff\x01\x86\x00\x00\x00\x00\x00\x79"
    __ZERO_CALIB = b"\xff\x01\x87\x00\x00\x00\x00\x00\x78"
    __SPAN_CALIB = b"\xff\x01\x88\x07\x00\x00\x00\x00\xA0"

    __connection = None
    __device = None

    def __init__(self, device):
        self.__device = device

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        self.__connection = serial.Serial(self.__device, timeout=1.0)

    def zero_calibrate(self):
        self.__connection.write(self.__ZERO_CALIB)

    def span_calibrate(self):
        self.__connection.write(self.__SPAN_CALIB)

    def get(self):
        # returns co2 concentration [ppm]
        self.__connection.write(self.__GET)
        result = self.__connection.read(9)
        co2 = result[2] * 0x100 + result[3]
        if not self.valid(result):
            logging.error("Check digit is not valid.")
        return co2

    def get_raw(self):
        # returns raw bytes
        self.__connection.write(self.__GET)
        result = self.__connection.read(9)
        return bytes(result)

    @staticmethod
    def valid(packet):
        checksum = 0xff - (sum(packet[1:8]) & 0xff) + 1
        if checksum == packet[8]:
            return True
        return False

    def close(self):
        self.__connection.close()
