from os import walk

mypath = "D:\REA-ICT\Python\pythonSource"
_, _, filenames = next(walk(mypath))

print(filenames)
