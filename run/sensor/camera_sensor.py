from time import sleep

from run.operation.camera_op import CAMERA_FORMAT


class Camera:
    def __init__(self, camera_instance, photos_dir, wait_before_still_in_seconds):
        self.camera_instance = camera_instance
        self.photos_dir = photos_dir
        self.wait_before_still_in_seconds = wait_before_still_in_seconds

    def take_photo(self, photo_name):
        self.camera_instance.start_preview()
        sleep(self.wait_before_still_in_seconds)
        self.camera_instance.capture(f'{self.photos_dir}/{photo_name}{CAMERA_FORMAT}')
        self.camera_instance.stop_preview()
        self.camera_instance.close()
