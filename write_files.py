from datetime import datetime
from os import getcwd, path, mkdir

dataList = []
inputData = ""
dt_string = ""
n = 1
dir = getcwd() + '\\data'


def write_file(path, data=None):
    ```Write input data to a file```
    with open(path, 'w') as file:
        file.write(data)


while not inputData == 'x':
    '''Take input and datetime : at least 4 lines'''
    try:
        inputData = input(f"Enter Line {n} (x to stop): ")  # Input
    except ValueError:
        print("Raised ValueError, please try again.")  # ValueError Raised
        continue
    else:
        # check if inputData is not x
        if inputData != 'x':
            # No ValueError Raised, continue interaction
            dataList.append(inputData)
            n += 1
        elif n < 5:
            print("Requires at least 4 lines.")
            inputData = False

now = datetime.now()  # get datetime
# format datetime:
# dd_mm_YY_H_M_S
# Using _ for Windows file system instead of : or /
formatted_dt = now.strftime("%d_%m_%Y_%H_%M_%S")
dt_string = formatted_dt

for i in range(len(dataList)):
    '''Write data to individual files, named by formatted date'''
    # Set default string
    formatted_dt = dt_string
    # Append unique ID
    formatted_dt += "_"
    formatted_dt += str(i)
    # Append text formatting
    formatted_dt += ".txt"
    # Combine path and file name for proper directory
    completeName = path.join(dir, formatted_dt)
    # Check if the directory exists
    if not path.exists(dir):
        try:
            mkdir(dir)  # Create directory if the specified path doesn't exist
        except OSError:
            print("Creation of the directory %s failed" %
                  dir)  # No permissions
        else:
            print("Succesfully created the directory %s" % dir)
            write_file(completeName, dataList[i])
    else:
        write_file(completeName, dataList[i])
