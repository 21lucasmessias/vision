import cv2


class CountCars:
    def __init__(self):
        self.video = 'video.mp4'
        self.exit_hotkey = 'q'
        self.delay = 10

        self.offset_x = 460
        self.offset_y = 500
        self.cars_count = 0

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

    def ProcessFrame(self, frame):
        roi = frame[500:650, 460:660]

        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(roi, 100, 255, cv2.THRESH_BINARY)

        cv2.imshow('thresh', thresh)

        return thresh

    def HandleCarCounter(self, car_center_y):
        if(car_center_y > 600):
            self.cars_count = self.cars_count + 1

            print(self.cars_count)

    def FindCarAndDraw(self, frame, processed_frame):
        cars, h = cv2.findContours(
            processed_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.line(frame, (450, 600), (670, 600), (255, 0, 0))

        for(i, c) in enumerate(cars):
            (x, y, w, h) = cv2.boundingRect(c)

            if(w > 40 and h > 40):
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
