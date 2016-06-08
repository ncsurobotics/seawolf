#!/usr/bin/env python

# [test-RazorIMU.py]: a quick test script used to get the sparkfun IMU working
# 06/08: code in rx_thread is able to process IMU data at a rate of 49.2Hz.

from __future__ import division, print_function

import seawolf
import serial
import threading
import time
import sys
import struct

DEVICE_PATH = '/dev/ttyUSB0'


# whether to automatically syncronize the 
AUTO_SYNC = False

class IMU:
    def __init__(self):
        self.usb = None
        self.baud = 57600
        self.output_mode = None #b=binary, t=text
        
        # device data attributes
        self.yaw = None
        self.pitch = None
        self.roll = None
        self.fs = None
        
        # device protocol symbols and attributes
        self.SYNC_REQ = '#s12'
        self.SYNCHRONIZE_STRING = '#SYNCH12\r\n'
        self.MINIMUM_IMU_SAMPLE_RATE = 49 #Hz
        
        # parallel processing attributes
        self.rx_thread = None
        self.blocking = None
        self.kill_rx = 0
        self.synchronize_flag = 0
        self.auto_sync = None
        self.yaw_stream = None
        self.pitch_stream = None
        self.roll_stream = None
        self.fresh_data_event = threading.Event()
        self.rx_thread_lock = threading.Lock()
        
        # serial status flag
        self.serial_disconnect_error_flag = threading.Event()
        

    """Opens the USB port at "path"."""
    def connect(self, path, timeout=2, threaded=False, auto_sync=True, blocking=True):
        # connect usb port
        self.usb = serial.Serial(path, self.baud,timeout=timeout)
        self.blocking = blocking
        
        # use the readline function as a means of waiting for the device to reset
        self.usb.read()
        
        # configure for binary mode
        self.setOutputMode('b') 
        
        # 
        if threaded:
            self.rx_thread = threading.Thread(target=self.rxProcessLoop,
                                  name="rxProcessLoop",
                                  args=())
        else: 
            self.rx_thread = None
            
        # auto _sync
        self.auto_sync = auto_sync
            
    """Disconnect the USB port associated with the IMU"""
    def disconnect(self):
        if self.usb == None:
            print("Received disconnect signal, but IMU already not connected!")
            return
        
        if self.rx_thread:
            self.stopStream()
            
        self.usb.close()
        self.usb = None
        
    """
    Sets the output mode of the IMU device by sending it the appropiate
    command. 
    
    args
      mode:
        'b' tells the IMU to output in binary mode
        't' tells the IMU to output in textual mode
    """
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

    """
    sends byte string to IMU via USB.
    ARGS
      text- the string that will be sent to the IMU
    """
    def send(self, text):
        self.usb.write(text)
        
    """
    The main loop for processing the stream of data that gets sent by the IMU
    """
    def rxProcessLoop(self, *args):
        # assert flags
        self.kill_rx=0
        if self.auto_sync:
            self.synchronize_flag = 1
        
        state = 'sample'
        
        # vSTART FUNCTION
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
        # ^END FUNCTION
            
        i = 0
        timea = time.time()
        while self.kill_rx==0:
            # state: perform sync if necessary
            if state == 'sync':
            
                # clear buffer and submit sync reqeust
                self.usb.flush()
                self.usb.write(self.SYNC_REQ)
                
                # wait until synchronization is complete
                waitForSyncronize(self.usb, self.SYNCHRONIZE_STRING)
                
                # exit out of sync state
                state = 'sample'
                
            elif state == 'sample':
                # check loop time
                if i == 100:
                    timeb       = time.time()
                    loop_freq   = i/(timeb-timea)
                    self.fs     = loop_freq
                    print("IMU operating at %.1fHz." % loop_freq)
                    
                    if loop_freq < self.MINIMUM_IMU_SAMPLE_RATE:
                        seawolf.logging.log(seawolf.WARNING, "Significant IMU delay detected!")
                    
                    i = 0
                    timea = time.time()
                
                # state: waiting for data packet
                try:
                    (yaw,pitch,roll) = self.readHeading()
                    
                except serial.SerialException:
                    seawolf.logging.log(seawolf.WARNING, "IMU disconnection detected. Killing rx thread.")
                    
                    # raise error flag
                    self.serial_disconnect_error_flag.set()
                    
                    # unblock any waiting functions in other threads
                    self.fresh_data_event.set() 
                    break
                
                # acquire lock, and share data with rest of class
                self.rx_thread_lock.acquire()
                self.yaw_stream = yaw
                self.pitch_stream = pitch
                self.roll_stream = roll
                
                # report fresh data and release the lock
                self.fresh_data_event.set()
                self.rx_thread_lock.release()

            
            # handle signals for next iteration
            if self.synchronize_flag == 1:
                self.synchronize_flag = 0
                state = 'sync'
                
            # increment loop counter
            i += 1

    """
    Read the imu. WARNING: this only works if the IMU is in binary
    output mode!
    """
    def readHeading(self):
        # read a single USB packet
        raw_packet = self.usb.read(12)
        
        # process the packet data
        (yaw,pitch,roll) = struct.unpack('fff',raw_packet)

        # return data
        return (yaw,pitch,roll)
        
        
    """
    get the latest AHRS heading from the IMU. assumes streaming rx thread,
    is active.
    """
    def getHeading(self, streaming=True, blocking=None):
        # assert blocking function
        if blocking == None:
            blocking = self.blocking
            
        # check if the rx thread is running
        if self.rx_thread.isAlive()==False:
            if self.serial_disconnect_error_flag.isSet():
                raise serial.SerialException("IMU disconnected!")
            else:
                raise SystemError("Received getHeading command, but RX thread not running!")

        # if blocking, wait for fresh data. otherwise, just return 
        # "None" if data is not fresh.
        if blocking:
            # wait until fresh data is present
            self.fresh_data_event.wait()

        else:
            if self.fresh_data_event.isSet() == False:
                return None
                
        # regardless if blocking or not, we must wait until 
        # data is safe to read.
        self.rx_thread_lock.acquire()
        
        # read the data
        self.yaw = self.yaw_stream
        self.pitch = self.pitch_stream
        self.roll = self.roll_stream
        self.fresh_data_event.clear()
        
        # release the lock
        self.rx_thread_lock.release()
        
        return (self.yaw, self.pitch, self.roll)
            


    def streamTest(self): # <--pretty buggy. Just for testing purposes.
        if self.rx_thread.isAlive() == False:
            raise serial.SerialException("You cannot streamTest without running self.startStream() first!")
        
        def printStream(imu_obj):
            print(imu_obj)
            while 1:
                (yaw, pitch, roll) = imu_obj.getHeading()
                text = ("%.1f,%.1f,%.1f" % (yaw,pitch,roll))
                print(text)
       
        printThread = threading.Thread(target=printStream,
                                  name="rxProcessLoop",
                                  args=(self,))
        printThread.start()
            
        
    def startStream(self):
        self.rx_thread.start()
    
    def stopStream(self):
        # send a kill signal to the rx_thread
        self.kill_rx = 1
        
        # block until rx_thread is terminated
        while self.rx_thread.isAlive():
            pass
            
            
    def synchronize(self):
        if rx_thread:
            self.synchronize_flag = 1
        else:
            print("Nothing to synchronize!")
        
    
        

def main():
    seawolf.loadConfig("../conf/seawolf.conf") # <--Contains IP for connecting to hub
    seawolf.init("RazorIMU.py") #<--Gives program a name under hub
    
    # open IMU object
    imu = IMU()
    imu.connect(DEVICE_PATH,threaded=True, auto_sync=AUTO_SYNC)
    #imu.setOutputMode('t')
    
    # issue help text
    if AUTO_SYNC==False:
        print("auto_sync disabled! If you see strange values, be sure to hit\n"+
              "ENTER once the stream of data starts. This will immediately\n"+
              "synchronize the IMU stream parser with the frame head of the\n"+
              "IMU data stream.")
        
        raw_input("\t\t  <Hit ENTER to continue>")
    
    # start streaming
    imu.startStream()
    imu.streamTest()
    
    
    # send a sync command and see what happens
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