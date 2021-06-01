# https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5
import cv2
from pyzbar import pyzbar
from format_file import format_datetime
from os import path, getcwd
from write_files import checkDir


def read_qrcodes(frame):
    qrcodes = pyzbar.decode(frame)
    isFound = False

    for qrcode in qrcodes:
        x, y, w, h = qrcode.rect

        # Decode QR code and draw rectangle
        qrcode_info = qrcode.data.decode('utf-8')

        # Format date and make the file name
        dt_string = format_datetime()
        dir = getcwd() + "\\data"
        completeName = path.join(dir, dt_string + '.txt')

        # Export information to text document
        with open(completeName, mode='w') as file:
            file.write("Recognized QR Code:" + qrcode_info)

        # Signal to stop program
        isFound = True

    return frame, isFound


def main():
    # Get dir
    dir = getcwd() + "\\data"

    # If directory exists or can be created:
    if checkDir(dir):
        # Turn on camera using OpenCV
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()

        # Run loop until 'Esc' is pressed
        while ret:

            ret, frame = camera.read()
            frame, isFound = read_qrcodes(frame)
            cv2.imshow('QR Code reader', frame)

            # If isFound is True, exit the loop
            if cv2.waitKey(1) & isFound:
                break

        # Release camera and close application window
        camera.release()
        cv2.destroyAllWindows()


# Call main function
if __name__ == '__main__':
    main()
