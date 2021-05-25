from datetime import datetime

dataList = []
timeList = []
inputData = ""
dt_string = ""
id = 0

while not inputData == 'x':
    '''Take input and datetime'''
    try:
        inputData = input("Enter Data (x to stop): ")  # Input
    except ValueError:
        print("Raised ValueError, please try again.")  # ValueError Raised
        continue
    else:
        # check if inputData is not x
        if inputData != 'x':
            # No ValueError Raised, continue interaction
            now = datetime.now()  # get datetime
            # format datetime:
            # dd/mm/YY H:M:S
            formatted_dt = now.strftime("%d_%m_%Y_%H_%M_%S")
            if dt_string == formatted_dt:  # Check if dates are the same
                new_string = formatted_dt
                new_string += "_"
                new_string += str(id)  # Add unique ID to datetime
                timeList.append(new_string)
                id += 1
            else:
                dt_string = formatted_dt
                timeList.append(dt_string)

            dataList.append(inputData)


for i in range(len(dataList)):
    '''Write data to individual files, named by formatted date'''
    # Create file name from timeList
    fileName = timeList[i]
    fileName += ".txt"
    with open(fileName, 'w') as file:
        file.write(dataList[i])
