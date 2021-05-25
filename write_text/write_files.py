from datetime import datetime

dataList = []
timeList = []
data = ""
dt_string = ""
id = 0

while not data == 'x':
    try:
        data = input("Enter Data (x to stop): ")  # Input
    except ValueError:
        print("Raised ValueError, please try again.")  # ValueError Raised
        continue
    else:
        # check if data is not x
        if data != 'x':
            # No ValueError Raised, continue interaction
            now = datetime.now()  # get datetime
            # format datetime:
            # dd/mm/YY H:M:S
            formatted_dt = now.strftime("%d/%m/%Y %H:%M")
            if dt_string == formatted_dt:  # Check if dates are the same
                new_string = formatted_dt
                new_string += " "
                new_string += str(id)  # Add unique ID to datetime
                timeList.append(new_string)
                id += 1
            else:
                dt_string = formatted_dt
                timeList.append(dt_string)

            dataList.append(data)
