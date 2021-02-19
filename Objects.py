import time

class Rectangle:
    lock = False
    corners = 0
    area = [186,185,184]
    time = 0
    environment_box = [0]
    higher_box = []
    lower_box = []
    environment_center = []
    higher_center = []
    lower_center = []
    start_time,scan_time = 0,0
    upper_corners = []


    def Start_time(self):
        self.start_time = time.time()
        return

    def Scan_time(self):
        self.scan_time = time.time() - self.start_time
        return self.scan_time