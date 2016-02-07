#!/usr/bin/env python
"""
Your task is as follows:
- read the provided Excel file
- find and return the min and max values for the COAST region
- find and return the time value for the min and max entries
- the time values should be returned as Python tuples

Please see the test function for the expected return format
"""

import xlrd
from zipfile import ZipFile
datafile = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    # All the references numbers (sheet, row, columns) begins with '0'
    sheet = workbook.sheet_by_index(0)

    ### example on how you can get the data
    # After that, 'sheet_data' python list contains all the data contained in the 1st sheet of the excel file
    sheet_data = [[sheet.cell_value(r, col) for col in range(sheet.ncols)] for r in range(sheet.nrows)]

    # In this example we iterate along of the rows. When we are in row 50, the data is printed
    # print "\nCells in a nested loop (row 50):"    
    # for row in range(sheet.nrows):
    #    for col in range(sheet.ncols):
    #        if row == 50:
    #            print sheet.cell_value(row, col),

    ### other useful methods:
    # print "\n\nROWS, COLUMNS, and CELLS:"
    # print "Number of rows in the sheet:", 
    # print sheet.nrows
    # print "Type of data in cell (row 3, col 2):", 
    # print sheet.cell_type(3, 2)
    # print "Value in cell (row 3, col 2):", 
    # print sheet.cell_value(3, 2)
    # print "Get a slice of values in column 3, from rows 1-3:"
    # print sheet.col_values(3, start_rowx=1, end_rowx=4)
    
    # print "\nDATES:"
    # print "Type of data in cell (row 1, col 0):", 
    # print sheet.cell_type(1, 0)
    # exceltime = sheet.cell_value(1, 0)
    # print "Time in Excel format:",
    # print exceltime
    # print "Convert time to a Python datetime tuple, from the Excel float:",
    # print xlrd.xldate_as_tuple(exceltime, 0)

    # Print several information about all the values of the column 1 (2nd column in excel):
    # max value, min value, sum of all the values, number of rows (except the header row), average value
    # position for max and min values
    cv = sheet.col_values(1, start_rowx=1, end_rowx=None)    
    maxval = max(cv)
    minval = min(cv)
    avgval = sum(cv) / float(len(cv))
    maxpos = cv.index(maxval) + 1
    minpos = cv.index(minval) + 1
    data = {
            'maxtime': xlrd.xldate_as_tuple(sheet.cell_value(maxpos, 0), 0),
            'maxvalue': round(maxval, 10),
            'mintime': xlrd.xldate_as_tuple(sheet.cell_value(minpos, 0), 0),
            'minvalue': round(minval, 10),
            'avgcoast': round(avgval, 10)
    }
    import pprint
    pprint.pprint(data)
    
    # Initialize the dictionary where we will store the result    
    data = {
            'maxtime': (0, 0, 0, 0, 0, 0),
            'maxvalue': 0,
            'mintime': (0, 0, 0, 0, 0, 0),
            'minvalue': 0,
            'avgcoast': 0
    }

    for row in range(sheet.nrows):
        if row == 1:
            data['maxvalue'] = round(sheet.cell_value(row, 1), 10)
            data['minvalue'] = round(sheet.cell_value(row, 1), 10)
            totalcost = sheet.cell_value(row, 1)
            data['maxtime'] = xlrd.xldate_as_tuple(sheet.cell_value(row, 0), 0)
            data['mintime'] = xlrd.xldate_as_tuple(sheet.cell_value(row, 0), 0)
        if (row > 1):
            totalcost = totalcost + round(sheet.cell_value(row, 1), 10)
            if sheet.cell_value(row, 1) > data['maxvalue']:
                data['maxvalue'] = round(sheet.cell_value(row, 1), 10)
                data['maxtime'] = xlrd.xldate_as_tuple(sheet.cell_value(row, 0), 0)
            if sheet.cell_value(row, 1) < data['minvalue']:
                data['minvalue'] = round(sheet.cell_value(row, 1), 10)
                data['mintime'] = xlrd.xldate_as_tuple(sheet.cell_value(row, 0), 0)

    data['avgcoast'] = round(totalcost / (sheet.nrows - 1), 10)

    return data


def test():
    open_zip(datafile)
    data = parse_file(datafile)

    # assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    # assert round(data['maxvalue'], 10) == round(18779.02551, 10)

    print data

test()