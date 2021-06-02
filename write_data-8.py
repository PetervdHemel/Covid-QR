from os import getcwd
from write_files import singleFile
from format_file import format_datetime
from uuid import uuid1

dataList = []
inputData = ""
n = 1
dir = getcwd() + "\\data"

# Returns formatted date and time in a string: dd_mm_YY_H_M_S
dt_string = format_datetime()
dataList.append(dt_string)  # Add to first value of dataList

while not inputData == "x":
    """Take input and datetime : at least 8 lines"""
    try:
        inputData = input(f"Enter Line {n} (x to stop): ")  # Input
    except ValueError:
        print("Raised ValueError, please try again.")  # ValueError Raised
        continue
    else:
        # check if inputData is not x
        if inputData != "x":
            # No ValueError Raised, continue interaction
            dataList.append(inputData)
            n += 1
        elif n < 9:
            print("Requires at least 8 lines.")
            inputData = False

# Random 14-bit sequence number generated
# Based on host ID, sequence number and current time
id = str(uuid1())

# Create file name
fileName = id + ".txt"

# Create file in the specified directory, using the file name and data list
singleFile(dir, fileName, dataList)
