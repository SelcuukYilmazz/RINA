import time

class Door:
    lock = False
    corners = 0
    area = 0
    time = 0
    box = []
    center = []
    start_time,end_time,scan_time = 0,0,0


    def Start_time(self):
        self.start_time = time.time()
        return

    def Scan_time(self):
        self.scan_time = time.time() - self.start_time
        return self.scan_time