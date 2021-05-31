import segno
from os import path, getcwd, walk
from write_files import checkDir

n = 1
dataList = []
userEntry = ' '


def createQR(fileData, dataString, fileName):
    # Concatenate fileData and dataString
    totalData = fileData + dataString

    # Create the QR Code
    qr = segno.make(totalData, micro=False)

    # Create file name
    fileName += ".png"

    dirCreated = checkDir(dir)
    if dirCreated:
        completeName = path.join(dir, fileName)

        qr.save(completeName, scale=5)


def singleFile(txtFiles, inputData):
    # Search for ID in txtFiles
    ifFound = False
    for string in txtFiles:
        if string == inputData:
            # Set found to True, save the string and break out of the loop
            ifFound = True
            fileName = string + '.txt'
            break
    if ifFound:
        # Read from file and compile
        completeName = path.join(dir, fileName)
        with open(completeName, 'r') as file:
            # Return the contents and name of the file
            return file.read(), string


# Start
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
    dataString = '_'.join(dataList)
else:
    dataString = ''

dir = getcwd() + "\\data"

if path.exists(dir):  # Check if the path exists in working directory
    _, _, filenames = next(walk(dir))  # Add all filenames to a list
else:  # If path doesn't exist
    print(f"Path {dir} does not exist.")
    print("Please write data files before attempting to read them,")
    print("or make sure they are in the working Directory.")

# Check if any files are present
if not filenames:
    print("No files found in working Directory.")
else:
    # Create list to store all .txt files in
    txtFiles = []
    for i in range(len(filenames)):
        '''Check which files are .txt and save them in a new List'''
        # Check last 4 characters of the string
        if filenames[i][-4:] == '.txt':
            txtFiles.append(filenames[i][:-4])  # Save file name without .txt

    print(txtFiles)
    ifMultiple = ''
    inputData = ''

    try:
        inputData = input("Enter a working data ID (none to exit): ")
    except ValueError:
        # ValueError Raised
        print("Raised ValueError, please try again.")
    else:
        if inputData:
            # Finds and opens the specified file if if found
            # Returns opened file data and file name
            fileData, name = singleFile(txtFiles, inputData)

            # If something is returned
            if fileData:
                createQR(fileData, dataString, name)
