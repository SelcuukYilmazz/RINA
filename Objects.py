import time

class Rectangle:
    lock = False
    corners = 0
    area = [185,184]
    time = 0
    higher_box = []
    lower_box = []
    higher_center = []
    lower_center = []
    start_time,scan_time = 0,0
    upper_corners = []
    decent_shape = True


    def Start_time(self):
        self.start_time = time.time()
        return

    def Scan_time(self):
        self.scan_time = time.time() - self.start_time
        return self.scan_time


class Circle:
    lock = False
    lock_coordinate = []
    box=[]
    area=0
    time = 0
    def Start_time(self):
        self.start_time = time.time()
        return

    def Scan_time(self):
        self.scan_time = time.time() - self.start_time
        return self.scan_time