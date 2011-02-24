
import threading
import time

class RateLimiter(object):
    """ Rate limit some incoming data

    A rate limiter has a callback and a maximum rate. A rate limiter accepts
    input via its 'provide' method and will call its callback with the most
    recently provided value at most max_rate times per second. Since only the
    most recent value is passed to the callback, input will be discarded if it
    comes in faster than the maximum rate.

    """

    def __init__(self, max_rate, callback):
        """ Create a new rate limiter

        Use the given max_rate and callback as described above

        """

        self.wait_time = 1.0 / max_rate
        self.callback = callback
        self.thread = threading.Thread(target=self.__caller)
        self.item_available = threading.Condition()
        self.item = None

        self.thread.daemon = True
        self.thread.start()

    def __caller(self):
        while True:
            my_item = None
            with self.item_available:
                while self.item == None:
                    self.item_available.wait()
                my_item = self.item
                self.item = None
            self.callback(my_item)
            time.sleep(self.wait_time)
        
    def provide(self, obj):
        """ Offer a new input

        Offer a new input value to the rate limiter

        """

        with self.item_available:
            self.item = obj
            self.item_available.notify()
