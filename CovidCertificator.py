import pandas as pd
import numpy as np
from os import getcwd, path
from write_files import checkDir

euCountries = {'België', 'Bulgarije', 'Cyprus', 'Denemarken', 'Duitsland',
               'Estland', 'Finland', 'Frankrijk', 'Griekenland',
               'Hongarije', 'Ierland', 'Italië', 'Kroatië', 'Letland',
               'Litouwen', 'Luxemburg', 'Malta', 'Nederland', 'Oostenrijk',
               'Polen', 'Portugal', 'Roemenië', 'Slovenië', 'Slowakije',
               'Spanje', 'Tsjechië', 'Zweden'}


def bsnLookup(bsn, datasheet):
    '''
    Look up if the user is present in the database.
    Returns an empty DataFrame if the BSN is not found in the datasheet.
    '''
    pdata = datasheet.loc[datasheet['BSN'] == bsn]
    if not len(pdata.index) == 0:
        return pdata
    else:
        print("Person data was not found, please enter a correct BSN.")
        return pdata


def userID():
    '''Let the user input their identification for the database comparison.'''
    while True:
        try:  # User input
            bsn = input("Please enter your valid BSN (8 digits): ")
        except ValueError:
            print("Raised ValueError.")  # ValueError Raised
        else:
            if len(bsn) == 8:  # Check to see if BSN is 8 digits
                try:
                    bsn = int(bsn)
                except ValueError:
                    print("Your BSN is not a number.")
                else:
                    return bsn
            elif not bsn:
                # If nothing was entered, return an empty BSN
                return bsn
            else:
                print("Your BSN is not 8 digits.")


def readDB():
    # Set directory
    dir = getcwd() + '\\data'
    # Check if directory exists
    dirCreated = checkDir(dir)
    if dirCreated:
        filename = path.join(dir, 'Covid1.xlsx')
        print("Attempting import of datasheets...")
        try:  # Read data sheets
            data1 = pd.read_excel(filename, sheet_name=0)
            data2 = pd.read_excel(filename, sheet_name=1)
        except FileNotFoundError:
            print(f"Datasheet file not found in directory {dir}, please make")
            print("sure that the valid Covid datasheet is available.")
            return data1, data2, False
        else:
            print(" ...Done.")
            # Check if data frames are not empty
            if not data1.empty or data2.empty:
                return data1, data2, True
            else:
                print("Incorrect datasheet, found to be empty.")


def diacriticCheck(country):
    diacriticCountries = ('Belgie', 'Italie', 'Kroatie', 'Roemenie',
                          'Slovenie', 'Tsjechie')

    for name in diacriticCountries:
        if country == name:
            country = country[:-1] + 'ë'

    return country


def userSelect():
    '''Let the user select a destination country to travel to.'''
    while True:
        try:  # User Input
            destination = input("Enter a valid EU country to travel to: ")
        except ValueError:
            print("Raised ValueError.")  # ValueError Raised
        else:
            if destination:  # If anything was entered.
                # Make sure the first letter is capitalized
                destination = destination.title()
                # Country Diacritic catching
                destination = diacriticCheck(destination)
                # Check if user entry is a european country
                if destination in euCountries:
                    print(f"Your destination is: {destination}.")
                    return destination  # Return country as a string
                else:
                    print("Please enter a correct European country.")
            else:
                # Return nothing to exit the program if nothing was entered
                print("Exit")
                return destination


def main():
    print("Welcome to the Covid Certification program.")
    print("This program takes a user destination and ID, then compares")
    print("the information to a database spreadsheet. When valid, a QR code")
    print("passport is created for travel to the destination country.")

    country = userSelect()
    if country:  # if a valid input was recorded. None exits the program.
        sheet1, sheet2, isValid = readDB()  # Fetch excel file and store sheets
        if isValid:  # Make sure the datasheet actually exists
            pdata = pd.DataFrame()  # Create empty dataframe
            bsn = ' '
            while pdata.empty and bsn:
                bsn = userID()  # Fetch user input: BSN
                # Check if BSN is not empty. Empty BSN means exit program
                if bsn:
                    pdata = bsnLookup(bsn, sheet1)  # Use BSN to look up User
                    print("Person data:")
                    print(pdata)
                else:
                    print("Exit")


# Call main function
if __name__ == "__main__":
    main()
