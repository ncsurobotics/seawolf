#!/usr/bin/env python

# [test-RazorIMU.py]: a quick test script used to get the sparkfun IMU working

from __future__ import division, print_function

import seawolf
import serial
import threading
import time
import sys
import struct

DEVICE_PATH = '/dev/ttyUSB0'
SYNC_REQ = '#s12'
SYNCHRONIZE_STRING = '#SYNCH12\r\n'

class IMU:
    def __init__(self):
        self.usb = None
        self.baud = 57600
        self.output_mode = None #b=binary, t=text
        
        # device data attributes
        self.x = None
        self.y = None
        self.z = None
        
        # parallel processing attributes
        self.rx_thread = None
        self.blocking = None
        self.kill_rx = 0
        self.synchronize_flag = 0
        
        #
        
    def connect(self, path, threaded=False):
        # connect usb port
        self.usb = serial.Serial(path, self.baud)
        
        # use the readline function as a means of waiting for the device to reset
        self.usb.read()
        
        # configure for binary mode
        self.setOutputMode('b') 
        
        # 
        if threaded:
            self.rx_thread = threading.Thread(target=self.rxProcess,
                                  name="rxProcess",
                                  args=())
        else: 
            self.rx_thread = None
            
    def disconnect(self):
        if self.usb == None:
            print("Received disconnect signal, but IMU already not connected!")
            return
        
        self.usb.close()
        self.usb = None
        
    def setOutputMode(self, mode):
        modes = {'b':'binary', 't':'text'}
        
        if mode in modes:
            if mode=='b':
                self.send('#ob')
                
            elif mode=='t':
                self.send('#ot')
                
            self.output_mode = mode
                
        else:
            print("Mode %s is not a valid mode." % mode)
            print("usage:")
            print("  mode=b: binary mode")
            print("  mode=t: text mode")
            raise IOError("Mode %s is not a valid mode." % mode)

    def send(self, text):
        self.usb.write(text)
            
    def startRXThread(self):
        # 
        '''
        <threadThing>(self.rx_thread)
        '''
        pass
        
    def rxProcess(self, *args):
        state = 'sample'
        
        def waitForSyncronize(device, sync_string):
            head = 0
            end = len(sync_string)

            while head < end:
                b = device.read()
                if b == sync_string[head]:
                    head += 1
                else:
                    head = 0
                    
            #print("---exited on (%s)---" % b)
            
        
        while self.kill_rx==0:
            # state: perform sync if necessary
            if state == 'sync':
            
                # clear buffer and submit sync reqeust
                self.usb.flush()
                self.usb.write(SYNC_REQ)
                
                # wait until synchronization is complete
                waitForSyncronize(self.usb, SYNCHRONIZE_STRING)
                
                # exit out of sync state
                state = 'sample'
                
            elif state == 'sample':
                # state: wait for loop timer if enabled
                #time.sleep(0.01)
                
                # state: waiting for data packet
                packet = self.readHeading()
                sys.stdout.write(packet)
                sys.stdout.flush()
                #   * write data packet to shared memory.
                #   * signal that me
                #   * go back to state 2.
            
            # handle signal for next iteration
            if self.synchronize_flag == 1:
                self.synchronize_flag = 0
                state = 'sync'

        
    def readHeading(self,x=0):
        n = 1
        output_packet = []
        
        for i in range(n):
            raw_packet = self.usb.read(12)
            
            (yaw,pitch,roll) = struct.unpack('fff',self.usb.read(12))

            processed_packet = ("%.0f,%.0f,%.0f\n" % (yaw,pitch,roll))
            
            output_packet.append( processed_packet )
        
        output_packet = ''.join(output_packet)
        return output_packet
    
    def setBlocking(self,blocking=True):
        self.blocking = blocking
        
    def streamTest(self):
        self.rx_thread.start()
        
    def stopStream(self):
        self.kill_rx = 1
        time.sleep(0.1)
        
    
        

def main():
    seawolf.loadConfig("../conf/seawolf.conf") # <--Contains IP for connecting to hub
    seawolf.init("RazorIMU.py") #<--Gives program a name under hub
    
    # open IMU object
    imu = IMU()
    imu.connect(DEVICE_PATH,threaded=True)
    #imu.setOutputMode('t')
    
    # start streaming
    imu.streamTest()
    time.sleep(1)
    
    # print help text
    print("\n\nWe are streaming IMU data.\n")
    time.sleep(1)
    
    # send a sync command and see what happend
    val = None
    while val !='q':
        if val == '':
            imu.synchronize_flag = 1
        if val == 'a':
            print("\n\nhello\n")
        val = raw_input()
    
    # close the program
    imu.stopStream()
    imu.disconnect()   
    seawolf.close() #<--Gracefully disconnects program from hub

main()