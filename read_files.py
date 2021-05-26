from os import walk, getcwd, path

txtFiles = []

dir = getcwd() + '\\data'
if path.exists(dir):
    _, _, filenames = next(walk(dir))
else:
    print(f"Path {dir} does not exist.")
    print("Please write data files before attempting to read them,")
    print("or make sure they are in the working Directory.")

if not filenames:
    print("No files found in working Directory.")
else:
    for i in range(len(filenames)):
        '''Check which files are .txt and save them in a new List'''
        if filenames[i][-4:] == '.txt':
            txtFiles.append(filenames[i][:-4])

    print(txtFiles)

    try:
        inputData = input("Enter a working data ID (date/time): ")
    except ValueError:
        print("Raised ValueError, please try again.")  # ValueError Raised
    else:
        # Check if inputData file exists in directory
        for string in txtFiles:
            if string[:-2] == inputData:
                print("inputData file exists in Directory")
                break
        dataOrder = []
        # Find all files with the same unique ID
        for string in txtFiles:
            if string.find(inputData, 0, 19) == 0:
                dataOrder.append(string[20:])  # Save order ID in dataOrder
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
