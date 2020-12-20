import cv2
import numpy as np


class CountCars:
    def __init__(self):
        self.video = 'video.mp4'
        self.exit_hotkey = 'q'
        self.delay = 10

        self.offset_x = 450
        self.offset_y = 445
        self.cars_count = 0

        self.found = False
        self.count = False
        self.lock = False

    def Start(self):
        video = cv2.VideoCapture(self.video)

        while video.isOpened():
            ret, frame = video.read()
            controlkey = cv2.waitKey(self.delay)

            if ret:
                processed_frame = self.ProcessFrame(frame)

                self.FindCarAndDraw(frame, processed_frame)
            else:
                break
            if controlkey == ord(self.exit_hotkey):
                break

        video.release()
        cv2.destroyAllWindows()

    def CarCenter(self, x, y, w, h):
        car_center_x = int(w / 2)
        car_center_y = int(h / 2)
        car_center_x = x + car_center_x
        car_center_y = y + car_center_y

        return car_center_x, car_center_y

    def ProcessRoi(self, roi):
        blank = np.zeros(roi.shape[:2], dtype='uint8')

        points = np.array([[48, 0], [175, 0],
                           [220, 300], [0, 300]], dtype=np.int32)

        mask = cv2.fillPoly(
            blank, [points], (255, 255, 255))

        roi = cv2.bitwise_and(roi, roi, mask=mask)

        return roi

    def ProcessFrame(self, frame):
        roi = frame[445:700, 450:675]

        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        thresh = cv2.adaptiveThreshold(
            roi, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 13, 5)

        roi = cv2.GaussianBlur(thresh, (5, 5), 1)

        roi = self.ProcessRoi(roi)

        cv2.imshow('roi', roi)

        return thresh

    def HandleCarCounter(self, car_center_y):
        self.found = car_center_y < 590 and not self.lock

        if(self.found):
            self.lock = True

        self.count = car_center_y > 610 and self.lock

        if(self.count):
            self.cars_count = self.cars_count + 1

            self.lock = False
            print(self.cars_count)

    def FindCarAndDraw(self, frame, processed_frame):
        cars, h = cv2.findContours(
            processed_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.line(frame, (450, 600), (670, 600), (255, 0, 0))

        for(i, c) in enumerate(cars):
            (x, y, w, h) = cv2.boundingRect(c)

            if(w > 60 and h > 70):
                cv2.rectangle(frame, (self.offset_x + x, self.offset_y + y),
                              (self.offset_x + x+w, self.offset_y + y+h), (0, 255, 0), 2)

                car_center_x, car_center_y = self.CarCenter(
                    self.offset_x + x, self.offset_y + y, w, h)

                cv2.circle(frame, (car_center_x, car_center_y),
                           4, (255, 0, 255), -1)

                self.HandleCarCounter(car_center_y)

                break

        cv2.imshow('frame', frame)


if __name__ == '__main__':
    CountCars().Start()
