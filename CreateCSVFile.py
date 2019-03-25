#Author: Nathan Roehl
#Fall 2018

import pandas as pd
import glob
from math import ceil


all_files = glob.glob("C:/Users/natha/Documents/College/Classes_Complete/EE890/Group Project/Zillow_Information/*.txt")
print(all_files)
lines = []
param = ["Floor size: "]
override = 0

YEAR_BUILT = 0
HEATING = 1
COOLING = 2
PARKING = 3
LOT = 4
BEDS = 5
ROOM_COUNT = 6
EXTERIOR = 7
STORIES = 8
MUNICIPALITY = 9
SCHOOL_DISTRICT = 10
DISHWASHER = 11
MICROWAVE = 12
RANGEOVEN = 13
REFRIGERATOR = 14
TRASH_COMPACTOR = 15
DRYER = 16
WASHER = 17
GARBAGE_DISPOSAL = 18
FREEZER = 19
FIREPLACE = 20
PATIO = 21
FENCED_YARD = 22
BATHS = 23
PRICESQFT = 24
SQFT = 25
PRICE = 26

final_param = []

for i in all_files:
    output_file = open(i, 'rt')
    data = output_file.read();
    output_file.close();
    lines.append(data.split('\n'))
    enterdata = data.find('\n')



line_length = int(len(lines))
new_list = []
list_full = []
for j in range(line_length):
    line_new = len(lines[j])
    print(lines[j])
    new_list = [None] * 27

    #Set default values for all possible features
    #If no data is provided while going over each house, the default is used
    #If data is provided while parsing, it will be over written
    new_list[YEAR_BUILT] = 1932
    new_list[HEATING] = 0
    new_list[COOLING] = 0
    new_list[PARKING] = 0
    new_list[LOT] = 4000
    new_list[BEDS] = 3
    new_list[ROOM_COUNT] = 5
    new_list[EXTERIOR] = 0
    new_list[STORIES] = 1
    new_list[MUNICIPALITY] = 0
    new_list[SCHOOL_DISTRICT] = 0
    new_list[PRICE] = 0
    new_list[PRICESQFT] = 0
    new_list[DISHWASHER] = 0
    new_list[MICROWAVE] = 0
    new_list[RANGEOVEN] = 0
    new_list[REFRIGERATOR] = 0
    new_list[TRASH_COMPACTOR] = 0
    new_list[DRYER] = 0
    new_list[WASHER] = 0
    new_list[GARBAGE_DISPOSAL] = 0
    new_list[FREEZER] = 0
    new_list[FIREPLACE] = 0
    new_list[PATIO] = 0
    new_list[FENCED_YARD] = 0
    new_list[BATHS] = 1
    new_list[SQFT] = 0

    #Can use dictionary to map zip codes to locations to fill out empty school districts and municipalities
    #default update is done when adding address to excel file
    #Not sure if theere are more zipcodes we have to worry about
    zip_codes = {'53217': 7 , '53211' : 6}

    #Three boolean variables used for keeping track of type of heating
    #Many docs repeat the heating information, these booleans help make sure each one is counted only once
    gas_added = False
    forced_air_added = False
    electric_added = False

    for k in range(line_new):
        if lines[j][k].__contains__(" WI "):                      #Finds address, only addresses should contain "WI"
            zip_index = lines[j][k].find("WI") + 3
            zip = lines[j][k][zip_index:]
            if zip in zip_codes:                                    #make sure zip is in zip codes to get correct mapping
                new_list[MUNICIPALITY] = zip_codes[zip]             #Set default municipality based on zip
                new_list[SCHOOL_DISTRICT] = zip_codes[zip]          #Set default school district based on zip

        elif lines[j][k].__contains__("Year Built: "):
            if "No Data" not in lines[j][k]:
                new_list[YEAR_BUILT] = (lines[j][k][11:])       #If there is a year, over write default value

        elif lines[j][k].__contains__("Floor size:"):
            override += 1
            sqft = lines[j][k][12:]
            index = sqft.index(" sq")
            new_list[SQFT] = sqft[:index].replace(",","")

        elif lines[j][k].__contains__("Heating: "):
            heat = lines[j][k][9:]
            if "Gas" in heat and not gas_added:                     #IF any of the heating options occur, increase value by one in excel file for house
                new_list[HEATING] = new_list[HEATING] + 1

                gas_added = True
            if "Forced Air" in heat and not forced_air_added:
                new_list[HEATING] = new_list[HEATING] + 1
                forced_air_added = True
            if "Electric" in heat and not electric_added:
                new_list[HEATING] = new_list[HEATING] + 1
                electric_added = True

        elif lines[j][k].__contains__("Cooling: "):
            cooling = lines[j][k][9:]
            if "Central" in cooling:
                new_list[COOLING] = 1                           #Setting one means there is air conditioning, else leave as default 0

        elif lines[j][k].__contains__("Parking: "):
            parking = lines[j][k][9:]
            if "Attached Garage" and "Electric" in parking:
                new_list[PARKING] = 5
            elif "Detached Garage" and "Electric" in parking:
                new_list[PARKING] = 2
            elif "Attached Garage" in parking:
                new_list[PARKING] = 4
            elif "Detached Garage" in parking:
                new_list[PARKING] = 1
            elif "Electric" in parking:
                new_list[PARKING] = 3

        elif lines[j][k].__contains__("Lot: "):
            lot_size = lines[j][k][5:]                                  #Get string value of lot size
            sqft_index = lot_size.find("sqft") - 1                      #adjust index of sqft to not include sqft tag at end
            if "No Data" in lot_size:                                   #If no data set size to default value
                lot_size = 4000
            elif sqft_index < 0:                                        #if sqft less than 0 means is in acres
                acre_index = lot_size.find("acre")
                conversion = float(lot_size[:acre_index].strip())
                lot_size = int(conversion * 43560)
            else:                                                       #If not "No Data" or acres means value is in sqft, simply remove sqft from string
                lot_size = int(lot_size[:sqft_index].replace(",",""))
                #int(a.replace(',', ''))
            new_list[LOT]= lot_size

        elif lines[j][k].__contains__("Beds: "):
           b = (lines[j][k][6:]).lower()
           if "studio" in b:
               b = 1
           new_list[BEDS] = b

        elif lines[j][k].__contains__("Room count: "):
            new_list[ROOM_COUNT]= (lines[j][k][12:])

        elif lines[j][k].__contains__("Exterior: "):
            exterior = lines[j][k][10:]
            if "Aluminum" in exterior or "Steel" in exterior:
                new_list[EXTERIOR] += 1                              #Set to one if exterior contains steel or aluminum

        elif lines[j][k].__contains__("Stories: "):
            s = int(ceil(float(lines[j][k][9:])))
            new_list[STORIES] = s                   #If no stories in information provided, will leave as default value 1

        elif lines[j][k].__contains__("Municipality: "):
            muni = (lines[j][k][14:]).lower()
            if "whitefish" in muni:
                new_list[MUNICIPALITY] = 7
            elif "shorewood" in muni:
                new_list[MUNICIPALITY] = 6
            elif "nicolet" in muni:
                new_list[MUNICIPALITY] = 5
            elif "fox" in muni:
                new_list[MUNICIPALITY] = 4
            elif "maple" in muni:
                new_list[MUNICIPALITY] = 3
            elif "glendale" in muni:
                new_list[MUNICIPALITY] = 2
            elif "milwaukee" in muni:
                new_list[MUNICIPALITY] = 1

        elif lines[j][k].__contains__("School district: "):

            school = (lines[j][k][17:]).lower()
            if "whitefish" in school:
                new_list[SCHOOL_DISTRICT] = 7
            elif "shorewood" in school:
                new_list[SCHOOL_DISTRICT] = 6
            elif "nicolet" in school:
                new_list[SCHOOL_DISTRICT] = 5
            elif "fox" in school:
                new_list[SCHOOL_DISTRICT] = 4
            elif "maple" in school:
                new_list[SCHOOL_DISTRICT] = 3
            elif "glendale" in school:
                new_list[SCHOOL_DISTRICT] = 2
            elif "milwaukee" in school:
                new_list[SCHOOL_DISTRICT] = 1

        elif lines[j][k].__contains__("Last sold: "):
            find = lines[j][k].find("$")
            new_list[PRICE] = int((lines[j][k][find + 1:]).replace(",",""))
        elif lines[j][k].__contains__("Last sale price/sqft: "):
            new_list[PRICESQFT] = int((lines[j][k][23:]).replace("$",""))
        elif lines[j][k].__contains__("Appliances included: "):

            line = lines[j][k][21:]

            if "Dishwasher" in line:
                new_list[DISHWASHER] = 1

            if "Microwave" in line:
                new_list[MICROWAVE] = 1

            if "Range / Oven" in line:
                new_list[RANGEOVEN] = 1

            if "Refrigerator" in line:
                new_list[REFRIGERATOR] = 1

            if "Trash compactor" in line:
                new_list[TRASH_COMPACTOR] = 1

            if "Dryer" in line:
                new_list[DRYER] = 1

            if "Washer" in line:
                new_list[WASHER] = 1

            if "Garbage disposal" in line:
                new_list[GARBAGE_DISPOSAL] = 1

            if "Freezer" in line:
                new_list[FREEZER] = 1

        elif lines[j][k].__contains__("Extra Information: "):

            extra_info = lines[j][k][19:]

            if "Fireplace" in extra_info:
                new_list[FIREPLACE] = 1
            if "Patio" in extra_info or "Deck" in extra_info or "Porch" in extra_info:
                new_list[PATIO] = 1
            if "Fenced Yard" in extra_info:
                new_list[FENCED_YARD] = 1

        elif lines[j][k].__contains__("Baths: "):
            bath = lines[j][k][7:]
            full = int(bath[0:1])
            half = float(bath[8:9]) / 2
            #half = int(bath[8:9])
            bath = full + half

            new_list[BATHS] = bath

    if int(new_list[SQFT]) == 0:
        x = float(new_list[PRICE])
        y = int(new_list[PRICESQFT])
        try:
            value = x/y
            new_list[SQFT] = int(value)
        except ZeroDivisionError:
            new_list[SQFT] = 0


    list_full.append(new_list)

table = pd.DataFrame(list_full)
print(table)
table.columns = ['Year Built','Heating','Cooling','Parking','Lot','Beds','Room count','Exterior','Stories','Municipality',
                 'School district','Dishwaser','Microwave','Range/Oven','Regrigerator','Trash Compactor','Dryer','Washer',
                 'Garbage Disposal','Freezer','Fireplace','Patio','Fenced Yard','Baths','Price/sqft','Sq/ft','Price']
table.to_csv("My_file.csv");

