from _thread import allocate_lock
from machine import Pin


class LockedPin(Pin):
    '''
    Thread safe pin for control across multiple threads.
    Use with:
    new_pin = ControlledPin(0)
    with new_pin as pin:
        pin.on()
        time.sleep(5)
        pin.off()
    '''

    def __init__(self, id, mode=-1, pull=-1, value=0):
        _pin = Pin(id, mode, pull, value=value)
        _lock = allocate_lock()

    def __enter__(self):
        self._lock.acquire()
        return self._pin

    def __exit__(self, exc_type, exc_value, traceback):
        self._lock.release()

    # methods for quick value changes

    def value(self, state_value):
        self._pin.value(state_value)

    def on(self):
        self._pin.on()

    def off(self):
        self._pin.off()
