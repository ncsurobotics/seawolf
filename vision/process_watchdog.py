
from time import time

class ProcessWatchdog(object):
    '''
    Sends and receives pings to make sure the process on the other side of a
    pipe is alive.
    
    There should be one ProcessWatchdog object on each side of the pipe for this
    process to work.  Timestamps are sent through the pipe and if a timestamp
    is not received on one end of the pipe within panic_interval seconds of the
    last sent timestamp, ping() will return False.

    ping() assumes that the ping_interval of both sides is the same.  For this
    reason, it is probably better for both ProcessPingers to have the same
    ping_interval.  Having a consistent panic_interval however is not
    important.
    
    '''

    def __init__(self, pipe, ping_interval, panic_interval):
        '''
        Arguments:

        pipe - The pipe which pings will be sent and received.
        ping_interval - Only ping this often (in seconds)
        panic_interval - If no pings have been received for this long (in
            seconds), ping() will return False.

        '''

        self.pipe = pipe
        self.ping_interval = ping_interval
        self.panic_interval = panic_interval

        t = time()
        self.last_ping_sent = t
        self.last_ping_received = t

        self.ping()

    def send_exit_signal(self):
        '''Sends an ExitSignal which will be raised on the other process.'''
        self.pipe.send(ExitSignal())

    def flush(self):
        '''Handles all objects waiting in the pipe.'''

        while self.pipe.poll():
            self.last_ping_received = self.pipe.recv()

            # Handle special signals
            if isinstance(self.last_ping_received, ExitSignal):
                raise self.last_ping_received

    def ping(self):
        '''Sends and receives a ping, but only if the ping_interval has passed.

        Returns True if the other end of the pipe is ok, False otherwise.

        This should be called about every ping_interval seconds or so.  If this
        function is not called every panic_interval seconds, the other end of
        the pipe may panic.

        '''
        t = time()

        # Send if ping_interval has passed
        if t - self.last_ping_sent > self.ping_interval:
            self.pipe.send(t)
            self.last_ping_sent = t

        # Receive if ping_interval has passed
        if t - self.last_ping_received > self.ping_interval:

            self.flush() # <-- Sets self.last_ping_received

            # Panic if panic_interval has passed
            if t - self.last_ping_received > self.panic_interval:
                return False

        return True

class ExitSignal(Exception):
    '''
    This is a special signal that can be sent from a process "A" through the
    pipe to tell process "B" that process "A" exited cleanly.  When this
    happens, the next call to ping() on process "B" raises this ExitSignal
    exception.  This signal is sent through the pipe by calling
    ProcessWatchdog.send_exit_signal().
    '''
    pass
