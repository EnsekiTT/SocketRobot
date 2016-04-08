# -*- coding: utf-8 -*-
"""Wave analyzer compornent for Socket Robot module.

This is wave analyzer compornent for Robot.
Read wave date and analyze it. (wave is not only audio wave)
"""
__auther__ = 'EnsekiTT'
__version__ = '0.1'

import pyaudio
import numpy as np

class SocketRobotWave():
    def __init__(self):
        print 'SocketRobotWave'
        self.p = pyaudio.pyaudio()

    def getDevices(self):
        self.deviceCount = self.pyaud.get_device_count()
        self.deviceInfo = self.pyaud.get_device_info_by_index()

    # show device information
    def showDevices(self):
        pass
    
    # set audio stream by device IDs
    def setStream(self, deviceIds):
        pass

    # get audio stream info
    def getStream(self):
        pass

    # record while n[sec]. 0 is inf
    def recordStream(self, n):
         pass

    # listen while n[sec]. 0 is inf
    def listenStream(self, n):
         pass

    # set file format
    def setFileFormat(self, str):
         pass

    # callback
    def callback(in_data, frame_count, time_info, status):
        return (in_data, pyaudio.paContinue)
    
    # filter
    def filter(self, in_data):
        out_data = in_data
        return out_data

    def iirFilter(self, 


if __name__ == '__main__':
    srw = SocketRobotWave()
