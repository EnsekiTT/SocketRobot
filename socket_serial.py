# -*- coding: utf-8 -*-
"""Serial compornent for Socket Robot module.

This is Serial compornent for Robot.
Send telemetry datas and receive control signals.
"""
__auther__ = 'EnsekiTT'
__version__ = '0.1'

import serial
import serial.tools.list_ports
import time


class SocketRobotSerial:

    """Serial comunicator."""

    def __init__(self):
        self.port = '/dev/tty.usbmodem14141'
        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.xonxoff_flow = False
        self.rtscts_flow = False
        self.dsrdtr_flow = False
        self.timeout = 10
        self.write_timeout = None
        self.inter_char_timeout = None

    def setSerialPort(self):
        self.ser = serial.Serial(
            port=self.port,
            baudrate=self.baudrate,
            bytesize=self.bytesize,
            parity=self.parity,
            stopbits=self.stopbits,
            timeout=self.timeout,
            xonxoff=self.xonxoff_flow,
            rtscts=self.rtscts_flow,
            writeTimeout=self.write_timeout,
            interCharTimeout=self.inter_char_timeout,
        )
        #self.ser.open()

    def stopSerialPort(self):
        self.ser.close()

    def readSerialPort(self):
        if self.ser.readable():
            return self.ser.readline()

    def getSerialPortName(self):
        print(list(serial.tools.list_ports.comports()))

if __name__ == '__main__':
    srs = SocketRobotSerial()
    srs.setSerialPort()
    start = time.time()
    while 1:
        print srs.readSerialPort(),
        if time.time()-start > 10:
            break
    srs.stopSerialPort()
