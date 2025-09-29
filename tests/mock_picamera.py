"""
Mock picamera module for testing on non-Raspberry Pi systems.
"""
class PiCamera:
    def __init__(self):
        self.start_preview = lambda: None
        self.stop_preview = lambda: None
        self.capture = lambda path: None
