import pandas as pd
import numpy as np
from os import getcwd, path
from write_files import checkDir
from datetime import datetime

euCountries = ('België', 'Bulgarije', 'Zuid-Cyprus', 'Denemarken', 'Duitsland',
               'Estland', 'Finland', 'Frankrijk', 'Griekenland',
               'Hongarije', 'Ierland', 'Italië', 'Kroatië', 'Letland',
               'Litouwen', 'Luxemburg', 'Malta', 'Nederland', 'Oostenrijk',
               'Polen', 'Portugal', 'Roemenië', 'Slovenië', 'Slowakije',
               'Spanje', 'Tsjechië', 'Zweden')


def genCert(cdata, pdata, passed, reason=None):
    '''

    '''
    print(f"Passed: {passed}")
    print(f"Reason(s): {reason}")


def validateCountryReqs(cdata, pdata, ptsReq, counter=0):
    '''
    Checks the country specific regulations and requirements, and adds to
    the requirements counter every time a requirement is met.
    Finally decides based on when point requirement is met whether the person
    passes the green certification requirement.
    '''
    # Initialize variable that states reason for pass or failure.
    reason = ''
    # Test if person has had any vaccination
    if not type(pdata[8]) is datetime:
        print(f"No vaccinations: {pdata[8]}")
    else:
        reason = f"Vaccination 1: {pdata[10]}\n"
        counter += 1
        if not pdata[9] == 'VOLDAAN':
            # Test if person had a second vaccination
            if not type(pdata) is datetime:
                print(
                    f"No second vaccination or incorrect date/time: {pdata[9]}"
                )
            else:  # If a second date for vaccination is registered.
                reason = f"Vaccination 1 & 2: {pdata[10]}\n"
                counter += 1
        else:  # If Vac2 == 'VOLDAAN'
            reason = f"Vaccination 1 & 2: {pdata[10]}\n"
            counter += 1

    # First test completed, time to check if it passes:
    if counter >= ptsReq:
        genCert(cdata, pdata, True, reason)


def validateJAorAZ(cdata, pdata):
    '''
    Checks if the person has had a Janssen or Astra Zenica vaccination, and if
    so, checks them off for a GREEN QR Certification.
    List index values:
    0: ID, 1: Voornaam, 2: Achternaam, 3: Email, 4: Geboortedatum, 5: BSN,
    6: Antistoffen, 7: Positief getest, 8: Vac1, 9: Vac2, 10: Vaccin,
    11: Geldige PCR test?
    '''
    if pdata[10] == 'AZ':
        genCert(cdata, pdata, True, 'Astra Zenica Vaccination')
    elif pdata[10] == 'JANS':
        genCert(cdata, pdata, True, 'Janssen Vaccination')
    else:
        validateCountryReqs(cdata, pdata, 2)


def cdataLookup(country, datasheet):
    '''
    Gets the index of a country and uses this to look up the proper row in
    datasheet 2, based on country ID (row A). Saves this row into a DataFrame.
    Returns a list representation of the DataFrame row.
    '''
    indexID = euCountries.index(country)
    row = datasheet.iloc[indexID]
    cdata = row.values.tolist()

    return cdata


def bsnLookup(bsn, datasheet):
    '''
    Look up if the user is present in the database.
    Returns an empty List if the BSN is not found in the datasheet.
    '''
    # Locate BSN in datasheet and save the entire row to pdata
    df = datasheet.loc[datasheet['BSN'] == bsn]
    df = df.iloc[0]
    pdata = []

    # Check if DataFrame has any contents (if BSN found)
    if not len(df.index) == 0:
        # Convert DataFrame to a List containing Person Data
        pdata = df.values.tolist()
        return pdata
    else:
        # If pdata does not have contents, return empty dataframe
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
            pdata = []  # Create empty list
            bsn = ' '
            while (not pdata) and bsn:
                bsn = userID()  # Fetch user input: BSN
                # Check if BSN is not empty. Empty BSN means exit program
                if bsn:
                    pdata = bsnLookup(bsn, sheet1)  # Use BSN to look up User
                else:
                    print("Exit")
            if pdata:  # If pdata is not an empty list
                print(pdata)
                # Returns a list of country relevant data
                cdata = cdataLookup(country, sheet2)
                print(cdata)
                # Check which vaccination standard the country has
                x = cdata[2]
                if x == '2  of  1 indien Jansen/Astra Zenica':
                    validateJAorAZ(cdata, pdata)


# Call main function
if __name__ == "__main__":
    main()
