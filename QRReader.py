# https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5
# Import spreadsheet modules
import numpy as np
import pandas as pd
from openpyxl import load_workbook

# Import image recognition modules
import cv2
from pyzbar import pyzbar

# Other modules
from format_file import format_datetime
from os import path, getcwd
from write_files import checkDir


def remfromDB(filename, index):

    # Open existing workbook
    book = load_workbook(filename=filename)

    sheet = book['Sheet1']

    # delete_rows(index, amount=1)
    sheet.delete_rows(index, 1)

    # Save the file to the path
    try:
        book.save(filename)
    except PermissionError:
        print("Permission Error:\n")
        print("Please close spreadsheet or give write permissions.")


def dbCheck(qrstring, dir, firstName, lastName):
    '''
    Separate the string into values, then extract the UUID and compare it
    against the First and Last names given, through the spreadsheet database.
    qrstring format:
    - Country of travel
    - UUID
    - BSN (if required)
    - Reason for acceptance or denial (if required)
    - PASS/DENY
    '''

    # Set directory
    filename = path.join(dir, 'Covid-id.xlsx')

    # Separate qrstring into a list with each line
    dataList = qrstring.splitlines()

    print(dataList)

    # Import datasheet
    print("Attempting import of datasheet...")
    try:
        datasheet = pd.read_excel(filename, sheet_name=0)
    except FileNotFoundError:
        print(f"Database not found in {dir = }")
    else:
        print("...Done.")

        # Locate UUID in datasheet, and save row as pdata
        if dataList[1]:
            df = datasheet.loc[datasheet['ID'] == dataList[1]]
        else:
            df = pd.DataFrame()

        # Checks if DataFrame has any contents (if UUID is found)
        if not len(df.index) == 0:
            # Select the row of the dataframe
            dfrow = df.iloc[0]

            # Convert DataFrame to a list
            pdata = dfrow.values.tolist()

            # Save index
            index = df.index[0] + 2

            # Check if names are the same as given on UUID match
            if firstName == pdata[1] and lastName == pdata[2]:
                remfromDB(filename, index)
                print("Passed Covid Check.")
            else:
                print("Your identification doesn't match your Covid passport.")
        else:
            print("Your Covid passport was already used or not legitimate.")


def read_qrcodes(frame, dir):
    qrcodes = pyzbar.decode(frame)

    for qrcode in qrcodes:
        x, y, w, h = qrcode.rect

        # Decode QR code and draw rectangle
        qrcode_info = qrcode.data.decode("utf-8")

        # Format date and make the file name
        dt_string = format_datetime()
        completeName = path.join(dir, dt_string + ".txt")

        # Export information to text document
        with open(completeName, mode="w") as file:
            file.write(qrcode_info)

        # Return frame and loop exit, as well as the qr info string
        return frame, True, qrcode_info

    return frame, False, None


def camControl(dir):
    # Turn on camera using OpenCV
    camera = cv2.VideoCapture(0)

    ret, frame = camera.read()

    if not ret:
        print("No Camera found")

    # Run loop until 'Esc' is pressed
    while ret:

        ret, frame = camera.read()
        frame, isFound, qrstring = read_qrcodes(frame, dir)
        cv2.imshow("QR Code reader", frame)

        # If isFound is True, exit the loop
        if cv2.waitKey(1) & isFound:
            break

    # Release camera and close application window
    camera.release()
    cv2.destroyAllWindows()

    return qrstring


def names():
    # Initialize vars
    firstName, lastName = '', ''
    try:  # Input
        firstName = input("Please enter First Name: ")
    except ValueError:
        print("Raised ValueError.")
        # Return nothing
        return '', ''
    else:
        if firstName:  # If anything was entered
            firstName = firstName.title()

            try:  # Input
                lastName = input("Please enter Last Name: ")
            except ValueError:
                print("Raised ValueError.")
                # Return nothing
                return '', ''
            else:
                if lastName:  # If anything was entered
                    lastName = lastName.title()

    return firstName, lastName


def main():
    # Get dir
    dir = getcwd() + "\\data"

    # Input traveler name
    firstName, lastName = names()

    # If first name and last name exist
    if firstName and lastName:
        # If directory exists or can be created:
        if checkDir(dir):
            # Start camera input until valid QR is found, return QR string
            qrstring = camControl(dir)
            if qrstring:
                # Separate string into list and adjust spreadsheet
                dbCheck(qrstring, dir, firstName, lastName)
            else:
                print("Empty QR code.")
        input()


# Call main function
if __name__ == "__main__":
    main()
