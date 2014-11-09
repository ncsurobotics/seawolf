import os
import cv2
from sys import argv

path = ''


def main():
    def nothing(x):
        pass

    if len(argv) > 1:
        path = argv[1]

    base_dir = os.getcwd()
    directory = os.path.join(base_dir, path)

    if not os.path.exists(directory):
        print "Invalid Path - Directory does not exist"
        exit()

    img_dirs = [
        image for image in os.listdir(directory) if os.path.splitext(image)[1][1:] in ['png', 'jpg', 'bmp']
    ]

    cv2.namedWindow('original')
    cv2.createTrackbar('Playback Speed:', 'original', 100, 200, nothing)

    counter = 0
    for img in sorted(img_dirs):
        frame = cv2.imread(os.path.join(directory, img))
        counter += 1
        cv2.putText(frame, "frame #: " + str(counter), (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1, cv2.CV_AA)
        cv2.putText(frame, "frame path: " + img, (50, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 1, cv2.CV_AA)
        cv2.imshow('original', frame)

        speed = cv2.getTrackbarPos('Playback Speed:', 'original')
        # 2000 * 100% = 20 fps, 8000 * 100% = 5 fps
        cv2.waitKey(int(8000 / (speed + 1)))


if __name__ == '__main__':
    main()
