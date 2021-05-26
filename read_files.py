from os import walk, getcwd, path

inputData = ''
dir = getcwd() + '\\data'  # Working directory

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
        if filenames[i][-4:] == '.txt':  # Check last 4 characters of the string
            txtFiles.append(filenames[i][:-4])  # Save file name without .txt

    print(txtFiles)

    while not inputData == 'x':
        # User data entry point
        print("\nInput 'x' to Quit at any time.")
        try:
            inputData = input("Enter a working data ID (date/time): ")
        except ValueError:
            print("Raised ValueError, please try again.")  # ValueError Raised
        else:
            if not inputData == 'x':
                # Create list for ordering the data files by order ID
                dataOrder = []
                for string in txtFiles:
                    # Remove the ordering ID and check against user entry
                    if string[:19] == inputData:
                        # Save order ID in dataOrder
                        dataOrder.append(string[20:])

                # Check if dataOrder is empty or not
                if dataOrder:
                    print("inputData file exists in Directory")

                    '''
                    Note: this step is probably optional because of how os.walk
                    iterates through the Directory, but it doesn't help to be
                    future or error-proof.
                    '''
                    # Sort the order of dataOrder
                    dataOrder.sort()
                    # Add data ID back to the ordered list, conver to tuple
                    for i in range(len(dataOrder)):
                        dataOrder[i] = inputData + '_' + dataOrder[i] + '.txt'
                    orderedFileNames = tuple(dataOrder)

                    # Read from files and compile
                    for fileName in orderedFileNames:
                        completeName = path.join(dir, fileName)
                        with open(completeName, 'r') as file:
                            print(file.read())
                else:
                    print("ID does not exist in Directory")
