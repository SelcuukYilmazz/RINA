import time
import numpy as np

class Rectangle:
    lock = False
    corners = 0
    area = np.array([185,184])
    time = 0
    higher_box = np.array([])
    lower_box = np.array([])
    higher_center =np.array([])
    lower_center = np.array([])
    start_time,scan_time = 0,0
    upper_corners = np.array([])
    decent_shape = True


    def Start_time(self):
        self.start_time = time.time()
        return

    def Scan_time(self):
        self.scan_time = time.time() - self.start_time
        return self.scan_time
class Circle:
    lock = False
    lock_coordinate = np.array([])
    box = np.array([])
    area=0
    time = 0
    def Start_time(self):
        self.start_time = time.time()
        return

    def Scan_time(self):
        self.scan_time = time.time() - self.start_time
        return self.scan_time