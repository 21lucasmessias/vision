import cv2

offset_x = 460
offset_y = 500


def car_center(x, y, w, h):
    car_center_x = int(w / 2)
    car_center_y = int(h / 2)
    car_center_x = x + car_center_x
    car_center_y = y + car_center_y

    return car_center_x, car_center_y


def process_frame(frame):
    roi = frame[500:650, 460:660]

    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(roi, 100, 255, cv2.THRESH_BINARY)

    return thresh


def handle_car_counter(car_center_y, cars_count):
    if(car_center_y > 600):
        cars_count = cars_count + 1

        print(cars_count)


def draw_find_car(frame, processed_frame, cars_count):
    center_y = 0

    cars, h = cv2.findContours(
        processed_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, (450, 600), (670, 600), (255, 0, 0))

    for(i, c) in enumerate(cars):
        (x, y, w, h) = cv2.boundingRect(c)

        if(w > 40 and h > 40):
            cv2.rectangle(frame, (offset_x + x, offset_y + y),
                          (offset_x + x+w, offset_y + y+h), (0, 255, 0), 2)

            car_center_x, car_center_y = car_center(
                offset_x + x, offset_y + y, w, h)

            cv2.circle(frame, (car_center_x, car_center_y),
                       4, (255, 0, 255), -1)

            handle_car_counter(car_center_y, cars_count)

            break

    cv2.imshow('frame', frame)


def Start():
    video = cv2.VideoCapture('video.mp4')

    while video.isOpened():
        ret, frame = video.read()
        controlkey = cv2.waitKey(10)

        cars_count = 0

        if ret:
            processed_frame = process_frame(frame)

            draw_find_car(frame, processed_frame, cars_count)
        else:
            break
        if controlkey == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    Start()
