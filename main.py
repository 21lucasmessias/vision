import cv2


def car_center(x, y, w, h):
    car_center_x = int(w / 2)
    car_center_y = int(h / 2)
    car_center_x = x + car_center_x
    car_center_y = y + car_center_y

    return car_center_x, car_center_y


def process_frame(frame):
    # roi

    #roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # threshhold binary, cars = white; road = black

    return roi


def draw_frame(frame, processed_frame):
    # find external countours in processed frame

    # draw the retangles arroud car and a circle in center

    cv2.rectangle(frame, (450, 350), (670, 620),
                  color=(0, 255, 0), thickness=2)

    cv2.ellipse(frame, car_center(0, 100, 100, 100),
                (1, 1), 0, 0, 360, color=(0, 255, 0))

    # add points of elipses to a array

    # draw a line to determine if a center of car pass throught

    cv2.line(frame, (450, 600), (670, 600), (255, 0, 0))

    # check if the points of elipses passed throught the line

    return frame


def


def Start():
    video = cv2.VideoCapture('video.mp4')

    while video.isOpened():
        ret, frame = video.read()
        controlkey = cv2.waitKey(5)

        if ret:
            processed_frame = process_frame(frame)

            drawned_frame = draw_frame(frame, processed_frame)

            cv2.imshow('frame', drawned_frame)
        else:
            break
        if controlkey == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    Start()
