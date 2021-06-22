# Import spreadsheet modules
import numpy as np
import pandas as pd
from openpyxl import load_workbook

# Import file modules
from os import getcwd, path
from write_files import checkDir
from PIL import Image

# Import QR modules
import segno

# Other modules
from datetime import datetime, date
from uuid import uuid1

# Initialize a tuple of all European countries
euCountries = ('België', 'Bulgarije', 'Zuid-Cyprus', 'Denemarken', 'Duitsland',
               'Estland', 'Finland', 'Frankrijk', 'Griekenland',
               'Hongarije', 'Ierland', 'Italië', 'Kroatië', 'Letland',
               'Litouwen', 'Luxemburg', 'Malta', 'Nederland', 'Oostenrijk',
               'Polen', 'Portugal', 'Roemenië', 'Slovenië', 'Slowakije',
               'Spanje', 'Tsjechië', 'Zweden')

# Initialize the directory
dir = getcwd() + '\\data'


def createQR(dataString, country, passed):
    '''
    Takes the QR data string and makes a file name, then uses segno to create
    a coloured QR certificate depending on pass/deny.
    Returns the complete name of the QR image.
    '''
    # Create the QR Code
    qr = segno.make(dataString, micro=False, error='M')

    # Create file name: country of travel _ date of creation
    fileName = country + date.today().strftime("_%d-%m-%Y") + '.png'

    # Set the complete name with the file path
    completeName = path.join(dir, fileName)

    # Save the relevant coloured QR code in the file path
    if passed:
        qr.save(completeName, scale=5, dark='green')
    else:
        qr.save(completeName, scale=5, dark='red')

    return completeName


def appendDB(pdata, cid, id):
    '''
    Appends the unique ID, and full name of the user that the Covid certificate
    is going to be created for to a different spreadsheet. This spreadsheet
    is used by the QR certificate reader program to verify the validity of
    the Covid certificate.
    Returns True if succesfully written to spreadsheet.
    '''
    print("Writing...")

    filename = path.join(dir, 'Covid-id.xlsx')

    # New dataframe with the same columns
    df = pd.DataFrame(
        {'ID': [id], 'Voornaam': [pdata[1]], 'Achternaam': [pdata[2]]})

    # Initiate writer on the user ID database
    try:
        writer = pd.ExcelWriter(filename, engine='openpyxl', mode='a')
    except PermissionError:
        print("Permission Error:\n")
        print("Please close spreadsheet or give write permissions.")
        return False
    else:
        # Open existing workbook
        writer.book = load_workbook(filename=filename)

        # Copy existing sheets
        writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)

        # Write out new sheet at the last row + 1 of cid
        df.to_excel(writer, index=False, header=False, startrow=len(cid) + 1)

        writer.close()

        print("...Done")

        return True


def genCert(cdata, pdata, cid, passed, country, reason=None):
    '''
    Creates a string variable that stores all information that will be present
    in the QR code. Formatted like:
    - Country of travel
    - UUID
    - BSN (if required)
    - Reason for acceptance or denial (if required)
    - PASS/DENY
    '''
    # Initialize information string for the QR certificate
    qrstring = country + '\n'

    # Generate unique ID for covid passport and add it to qrstring
    id = str(uuid1())
    qrstring += id + '\n'

    # Add unique id and user name(s) to covid id database
    appended = appendDB(pdata, cid, id)

    if appended:
        if cdata[5] == 'Ja':
            # BSN required on certificate
            qrstring += str(pdata[5]) + '\n'
        else:
            # BSN not required on certificate
            qrstring += '\n'

        if cdata[6] == 'Ja':
            # Reason required on certificate
            qrstring += reason[:-2] + '\n'
        else:
            # Reason not required on certificate
            qrstring += '\n'

        if passed:
            # If the person can travel to country
            qrstring += 'PASS'
        else:
            # If the person cannot travel to country
            qrstring += 'DENY'

        # Create the QR image
        qrName = createQR(qrstring, country, passed)

        # Open the QR image using PIL
        with Image.open(qrName) as im:
            im.show()


def covidpositiveTest(cdata, pdata, reason, counter):
    '''
    Check if a country accepts earlier Covid Positive ratings as a vaccination,
    whether the person has had them, or the timespan in which it is accepted.
    '''
    if cdata[3] == 'Nee':
        print("Country does not accept Covid positive tests.")
        return reason, counter

    # Save timespans for country specific covid positive tests
    if len(cdata[3]) == 33:
        try:
            print(int(cdata[3][24:25]))
            covidTime = int(cdata[3][24:25])
        except ValueError:
            print("Country has incorrect covid positive standards.")
            return reason, counter
    else:
        try:
            print(int(cdata[3][24:26]))
            covidTime = int(cdata[3][24:26])
        except ValueError:
            print("Country has incorrect covid positive standards.")
            return reason, counter

    # Test if person has had any positive Covid tests in the past
    if not pdata[7] == 'nvt':
        start_date = pdata[7]

        # Set today as a date in d/m/y. strftime makes it a string.
        today = date.today().strftime("%d/%m/%Y")
        # dd/mm/YY as a datetime.datetime
        end_date = datetime.strptime(today, "%d/%m/%Y")

        print(f"type start_date: {type(start_date)}")
        print(f"type end_date: {type(end_date)}")

        # Calculate the number of months since positve test
        num_months = (end_date.year - start_date.year) * \
            12 + (end_date.month - start_date.month)
        print(f"Number of months: {num_months}")

        if covidTime >= num_months:  # If person follows country regulation
            counter += 1

        # Update reason
        reason += f"Previously had Covid {num_months} months ago, "
    else:
        reason += "Has not had Covid previously, "

    return reason, counter


def pcrTest(cdata, pdata, reason, counter):
    '''Check PCR test results, return the updated counter and reason'''
    if cdata[4] == 'Ja':  # If country accepts all PCR tests
        if not pdata[11] == 'Nee':  # If PCR test is yes
            reason += "PCR Tested, "
            counter += 1
            return reason, counter
    # If country accepts PCR test with time limit
    elif cdata[4][:3] == 'Ja,':
        if not pdata[11] == 'Nee':  # If PCR test is yes
            try:
                # Validate if the input is proper and convert to integer
                pcrTime = int(pdata[11][4:6])
            except TypeError:
                print("Invalid PCR time data.")
            else:
                # If the country time regulation for PCR tests >= person
                if int(cdata[4][13:15]) >= pcrTime:
                    reason += f"PCR Test {pcrTime}h ago, "
                    counter += 1
                    return reason, counter

    # If PCR not accepted in cdata or no valid PCR test found
    reason += "No/invalid PCR, "
    return reason, counter


def vaccineTest(cdata, pdata, reason, counter):
    '''
    Test if person has had any vaccination. Return updated counter and reason
    '''
    if not type(pdata[8]) is datetime:
        print(f"No vaccinations: {pdata[8]}")
        reason = "No vac, "
        return reason, counter
    else:
        reason = f"Vac x1: {pdata[10]}, "
        counter += 1
        if not pdata[9] == 'VOLDAAN':
            # Test if person had a second vaccination
            if not type(pdata[9]) is datetime:
                print(
                    f"No second vaccination or incorrect date/time: {pdata[9]}"
                )
                return reason, counter
            else:  # If a second date for vaccination is registered.
                reason = f"Vac x2: {pdata[10]}, "
                counter += 1
                return reason, counter
        else:  # If Vac2 == 'VOLDAAN'
            reason = f"Vac x2: {pdata[10]}, "
            counter += 1
            return reason, counter


def validateCountryReqs(cdata, pdata, ptsReq, counter=0):
    '''
    Checks the country specific regulations and requirements, and adds to
    the requirements counter every time a requirement is met.
    Finally decides based on when point requirement is met whether the person
    passes the green certification requirement.
    '''
    # Initialize variable that states reason for pass or failure.
    reason = ''

    # Test vaccines if counter is not yet negative from unknown vaccine
    if counter == 0:
        reason, counter = vaccineTest(cdata, pdata, reason, counter)
    else:
        # Reset the counter to 0 and add unknown vaccine to reason
        counter = 0
        reason = "N/A vac, "

    # First test completed, time to check if it passes:
    if counter >= ptsReq:
        return True, reason
    else:
        # Test PCR
        reason, counter = pcrTest(cdata, pdata, reason, counter)

        # Second test completed, time to check if it passes:
        if counter >= ptsReq:
            return True, reason
        else:
            # Test possible previous Covid case
            reason, counter = covidpositiveTest(cdata, pdata, reason, counter)

            # Third test completed, time to check if it passes:
            if counter >= ptsReq:
                return True, reason
            else:  # If none of the requirements are met, return failure
                return False, reason


def validaterecVacc(cdata, pdata):
    '''
    Checks if the person has had any vaccines that are unknown or not EMA
    recognized. Continues to validate the country requirements with a negative
    counter if so.
    '''
    counter = 0
    if pdata[10] == 'ONB':
        reason, counter = vaccineTest(cdata, pdata, '', counter)
        if counter == 1:
            passed, reason = validateCountryReqs(cdata, pdata, 1, -1)
            return passed, reason
        else:
            passed, reason = validateCountryReqs(cdata, pdata, 1, -2)
            return passed, reason
    else:
        passed, reason = validateCountryReqs(cdata, pdata, 1)
        return passed, reason


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
        return True, 'Astra Zenica Vaccination'
    elif pdata[10] == 'JANS':
        return True, 'Janssen Vaccination'
    else:
        passed, reason = validateCountryReqs(cdata, pdata, 2)
        return passed, reason


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
    # Check if directory exists
    dirCreated = checkDir(dir)
    if dirCreated:
        filename1 = path.join(dir, 'Covid1.xlsx')
        filename2 = path.join(dir, 'Covid-id.xlsx')
        print("Attempting import of datasheets...")
        try:  # Read data sheets
            data1 = pd.read_excel(filename1, sheet_name=0)
            data2 = pd.read_excel(filename1, sheet_name=1)
            data3 = pd.read_excel(filename2, sheet_name=0)
        except FileNotFoundError:
            print(f"Datasheet file not found in directory {dir}, please make")
            print("sure that the valid Covid datasheet is available.")
            return data1, data2, data3, False
        else:
            print(" ...Done.")
            # Check if data frames are not empty
            if not data1.empty or data2.empty:
                return data1, data2, data3, True
            else:
                print("Incorrect datasheet, found to be empty.")


def diacriticCheck(country):
    '''Checks if user inputted country has a diacritic in its name.'''
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
        # Fetch excel file and store sheets
        sheet1, sheet2, cid, isValid = readDB()
        if isValid:  # Make sure the datasheet actually exists
            pdata = []  # Create empty list
            bsn = ' '
            while (not pdata) and bsn:
                bsn = userID()  # Fetch user input: BSN
                # Check if BSN is not empty. Empty BSN means exit program
                if bsn:
                    pdata = bsnLookup(bsn, sheet1)  # Use BSN to look up User
                else:
                    print("Exit: no BSN given.")
            if pdata:  # If pdata is not an empty list
                print(pdata)
                # Returns a list of country relevant data
                cdata = cdataLookup(country, sheet2)
                print(cdata)
                # Check which vaccination standard the country has
                vaccStandard = cdata[2]
                if vaccStandard == '2  of  1 indien Jansen/Astra Zenica':
                    # Checks if person has Janssen or AZ vaccine
                    passed, reason = validateJAorAZ(cdata, pdata)
                elif vaccStandard == '1, ongeacht welk type':
                    passed, reason = validateCountryReqs(cdata, pdata, 1)
                elif vaccStandard == '1, alleen goedgekeurde vaccins':
                    # Checks if person has unrecognized vaccine
                    passed, reason = validaterecVacc(cdata, pdata)
                elif vaccStandard == 2:
                    passed, reason = validateCountryReqs(cdata, pdata, 2)

                genCert(cdata, pdata, cid, passed, country, reason)


# Call main function
if __name__ == "__main__":
    main()
