import segno
from uuid import uuid1
from os import path, getcwd
from write_files import checkDir

print("This script will generate a QR Code")
try:
    link = input("Enter valid Website URL Address: ")
except ValueError:
    print("Raised ValueError, please try again.")  # ValueError Raised
else:
    dir = getcwd() + "\\data"
    qr = segno.make(link, micro=False)

    # Random 14-bit sequence number generated
    # Based on host ID, sequence number and current time
    id = str(uuid1())

    # Create file name
    fileName = id + ".png"

    dirCreated = checkDir(dir)
    if dirCreated:
        completeName = path.join(dir, fileName)

        qr.save(completeName)
