from os import path, mkdir


def write_file(path, data=None):
    '''Write input data to a file'''
    with open(path, 'w') as file:
        file.write(data)


def createFiles(dir, dataList=None, nameStrings=None):
    for i in range(len(dataList)):
        # Combine path and file name for proper directory
        completeName = path.join(dir, nameStrings[i])
        # Check if the directory exists
        if not path.exists(dir):
            try:
                # Create directory if the specified path doesn't exist
                mkdir(dir)
            except OSError:
                print("Creation of the directory %s failed" %
                      dir)  # No permissions
            else:
                print("Succesfully created the directory %s" % dir)
                write_file(completeName, dataList[i])
        else:
            write_file(completeName, dataList[i])
