import segno
from uuid import uuid1
from os import path, getcwd
from write_files import checkDir

n = 1
dataList = []
userEntry = " "

while userEntry:
    print("This script will generate a QR Code from multiple lines")
    print("Enter an empty line to quit")
    try:
        userEntry = input(f"Enter text value number {n}: ")  # User Input
    except ValueError:
        print("Raised ValueError, please try again.")  # ValueError Raised
    else:
        if userEntry:
            n += 1

            # Append user input to list
            dataList.append(userEntry)
        else:
            print("Exit")
            continue

if dataList:
    # Concatenate User Entries
    dataString = "_".join(dataList)

    dir = getcwd() + "\\data"

    # Create the QR Code
    qr = segno.make(dataString, micro=False)

    # Random 14-bit sequence number generated
    # Based on host ID, sequence number and current time
    id = str(uuid1())

    # Create file name
    fileName = id + ".png"

    dirCreated = checkDir(dir)
    if dirCreated:
        completeName = path.join(dir, fileName)

        qr.save(completeName, scale=5)
