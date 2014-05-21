import cv2
from sys import argv
import os
import time


def img_to_video():
    path = ''

    if (len(argv) > 1):
        path = argv[1]

    BASE_DIR = os.getcwd()
    directory = os.path.join(BASE_DIR, path)

    images = [image for image in os.listdir(directory) if os.path.splitext(image)[1][1:] in ['png', 'jpg', 'bmp']]

    out = cv2.VideoWriter(
        'output.avi', cv2.cv.FOURCC('X', 'V', 'I', 'D'), 20.0, (640, 480))

    for image in sorted(images):
        img = cv2.imread(os.path.join(directory, image))
        out.write(img)

    out.release()


def main():
    def nothing(x):
        pass

    path = ''

    if (len(argv) > 1):
        path = argv[1]

    BASE_DIR = os.getcwd()
    directory = os.path.join(BASE_DIR, path)

    img_dirs = [image for image in os.listdir(directory) if os.path.splitext(image)[1][1:] in ['png', 'jpg', 'bmp']]

    cv2.namedWindow('original')
    cv2.createTrackbar('Playback Speed:', 'original', 100, 200, nothing)

    counter = 0
    for img in sorted(img_dirs):
        frame = cv2.imread(os.path.join(directory, img))
        counter += 1
        cv2.putText(frame, "frame #: " + str(counter), (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1, cv2.CV_AA)
        cv2.putText(frame, "frame path: " + img, (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1, cv2.CV_AA)
        cv2.imshow('original', frame)

        speed = cv2.getTrackbarPos('Playback Speed:', 'original')
        # 100% = 20 fps
        cv2.waitKey(int(2000 / speed))


if __name__ == '__main__':
    main()
