from os import path, mkdir


def write_file(path, data):
    '''Write input data to a file'''
    with open(path, 'w') as file:
        file.write(data)


def checkDir(dir):
    '''
    Checks if directory exists, and makes one if it doesn't.
    Returns false if unable to make a directory.
    '''
    # Check if the directory exists
    if not path.exists(dir):
        try:
            # Create directory if the specified path doesn't exist
            mkdir(dir)
        except OSError:
            print("Creation of the directory %s failed" %
                  dir)  # No permissions
            return False
        else:
            print("Succesfully created the directory %s" % dir)
            return True
    else:
        print("Directory %s exists" % dir)
        return True


def separateFiles(dir, dataList=None, nameStrings=None):
    dirCreated = checkDir(dir)
    if dirCreated:
        for i in range(len(dataList)):
            '''Create/find directory and write data to different files'''
            # Combine path and file name for proper directory
            completeName = path.join(dir, nameStrings[i])
            write_file(completeName, dataList[i])


def singleFile(dir, name, dataList=None):
    dirCreated = checkDir(dir)
    if dirCreated:
        completeName = path.join(dir, name)
        data = ''
        for item in dataList:
            data = data + '\n' + item
        write_file(completeName, data)
