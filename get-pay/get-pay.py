#!/usr/bin/python3
#!./Python-3.4.3/python

"""
Should be able to enter which day you want it to start from.
Will throw an error if it is not a Monday.
"""

from time import strptime, strftime, mktime
from datetime import timedelta, datetime, date
from os import _exit, system

name_xls = "Roster 01.07.13.xls"
name_csv = "Roster 01.07.13.csv"
name_roster_sheet = "Current Roster"
epoch_week1 = datetime.fromtimestamp(mktime(strptime("13/04/2015", "%d/%m/%Y")))

len_left_filler = 22
# The number of columns for each day
# Name | Start | finish

len_group_vert = 13
names = ["Brianna", "Daniel", "Grace", "Heather", "Julia", "Karen", "Kate", "Kirsten", "Laura", "Lynda", "Meghan", "Sharyn", "Tess"]

"""
Function definitions
"""

# Credit to: http://stackoverflow.com/questions/26029095/python-convert-excel-to-csv
""" Python 2 package.
#system("export PYTHONPATH=/usr/local/lib/python2.7/dist-packages:$PYTHONPATH")
def Excel2CSV(ExcelFile, SheetName, CSVFile):
    import xlrd
    import csv
    workbook = xlrd.open_workbook(ExcelFile)
    worksheet = workbook.sheet_by_name(SheetName)
    csvfile = open(CSVFile, 'wb')
    wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

    for rownum in range(0, worksheet.nrows):
        wr.writerow(
            list(x.encode('utf-8') if type(x) == type(u'') else x
                 for x in worksheet.row_values(rownum)))
    print("closing")
    csvfile.close()
"""
#13/04/2015

def print_divider():
    print("====================")

# Takes a string, returns a datetime object
def get_datetime_obj(inp_str):
    date_inp = strptime(inp_str, "%d/%m/%Y")
    date_inp_dt = datetime.fromtimestamp(mktime(date_inp))
    return date_inp_dt

# Returns a datetime object
def get_date():
    print("Please enter the date of a Week 1 Monday.\nFormat: dd/mm/yyyy")
    date_inp = input(">> ")
    if date_inp == "":
        print("No input. Using the most recent Week 1 Monday as default.")
        # Gets last monday.
        last_mon = datetime.today() - timedelta(days=date.today().weekday())

        if(last_mon - epoch_week1).days == 0:
            return last_mon
        else:
            return last_mon - timedelta(days=7)
    try:
        date_inp_dt = get_datetime_obj(date_inp)
        if date_inp_dt.weekday() != 0:
            print("Please enter the date of a Monday")
            return get_date()
        print("Date accepted.")
        return date_inp_dt
    except ValueError:
        print("That was not the correct format. Try again...")
        return get_date()
    except Exception as e:
        print("Unexpected error. Terminating...")
        print(str(e))
        _exit(1)

#13/04/2015

def get_name():
    name_inp = input("Enter your name.\nType help for a list of names.\n>> ").title()
    if name_inp == "":
        print("No name inputted. Using Daniel as default.")
        return "Daniel"
    elif name_inp == "Help":
        print("The options are:")
        print(names[0], end="")
        # [names[i] for i in range(0, len(names)) if i > 0]
        for name in names[1:]:
            print(", " + name, end="")
        print()
        return get_name()
    elif name_inp in names:
        print("Name accepted.")
        return name_inp
    else:
        print("%s is not a valid name option. Type 'help' for help." % name_inp)
        return get_name()


#Object Day():
#    def __init__(self):



# Takes a datetime object, returns an array of tuples (start_time, finish_time, weekend?)
def get_block(start_date):
    days = []

# Takes a str and a datetime obj.
def print_date(title_n, datetime_obj):
    # Converts the datetime object to a time object for printing
    print("%10s: %s | %s" % (title_n.title(), strftime("%d/%m/%Y", datetime_obj.timetuple()), strftime("%a, %d %b %Y", datetime_obj.timetuple())))

# Takes the entire csv content, returns a fortnight still in list format.
def get_fortnight(block, start_date):
    week1_notation = "WEEK 1"
    week2_end_notation = "Consulting"
    week1_start = len(block) - 2

    while week1_start >= 0:
        if(block[week1_start].split(',')[0] == week1_notation):
            """
            print(week1_start)
            print(start_date)
            print(get_datetime_obj(block[week1_start+1].split(',')[1]).date())
            print(start_date.date())
            """
            if(get_datetime_obj(block[week1_start+1].split(',')[1]).date() == start_date.date()):
                print("Found the start date.")
                break
        week1_start -= 1

    if week1_start == -1:
        print("Couldn't find the start date previously specified.")
        print("Terminating...")
        _exit(1)

    print("Full fortnight available, continuing.")
    return block[week1_start:week1_start + len_group_vert*2 - 1]

"""
Program start
"""

# A datetime obejct for "arithmetic"
start_date = get_date()

print_divider()
print_date("Start", start_date)
print_date("Finish", start_date + timedelta(days=13))
print_date("Pay date", start_date + timedelta(days=17))
print_divider()

name = get_name()

#Excel2CSV(name_xls, name_roster_sheet,name_csv)

contents = []
try:
	with open(name_csv, "rb") as f:
		contents = f.readlines()
except FileNotFoundError:
	print("Roster could not be found. It should be called:")
	print(name_csv)
	_exit(1)

contents2 = []
# Getting rid of all the unecessary empty columns at the start and empty rows.
for line in contents:
    contents2.append(line[len_left_filler:].decode('utf-8'))
    # ??? [len_left_filler:] ???
    """
    The below doesn't take into account lines that are normally empty but
    sometimes have content. Hence just leave empty lines in.
    from re import sub
    nline = sub('[-,\n\r]', '', line.decode('utf-8')).replace(" ", "")
    #print(nline)
    if nline.isalnum():
        output.append(line[len_left_filler:].decode('utf-8'))
    """

contents = contents2
contents2 = None

"""
# Getting last 2 fortnights (last 4 weeks).
four_weeks = four_weeks[len(four_weeks) - len_group_vert*4:]
for i in four_weeks:
    print(i)
"""

fortnight = get_fortnight(contents, start_date)

#
# Returns list with 4 elements, one for each week.
# Each element: {day: {person: (start, end)}}
# i.e. the day of the week as the key to a value which is a dict which
# has a person as the key and the value being a tuple with start and end.

# Returns dict like this:
# {person: [(start, finish, weekend?), (etc)]
def fortnight_processor(fortnight):
    len_group_horiz = 3
    output = {}
    vert_point = 2
    horiz_point = 1
    while vert_point < len(fortnight):
        row = fortnight[vert_point].split(',')
        # Ignoring rows with no meaningful data by checking for names in col1.
        if(row[horiz_point].title() not in names):
            pass
        else:
            #print("first name: %s" % row[horiz_point])
            while(horiz_point < 7*len_group_horiz):
                name = row[horiz_point]
                # Ignoring empty slots
                if name == "":
                    horiz_point += len_group_horiz
                    continue
                start = row[horiz_point + 1]
                finish = row[horiz_point + 2]
                # Checking if we're looking at a weekend.
                if(horiz_point > 5*len_group_horiz):
                    output_tuple = (start, finish, True)
                else:
                    output_tuple = (start, finish, False)
                try:
                    output[name].append(output_tuple)
                except KeyError:
                    output[name] = []
                    output[name].append(output_tuple)
                except Exception as e:
                    print("An unexpected error occured:")
                    print(str(e))
                    print("Terminating...")
                    _exit(1)
                horiz_point += len_group_horiz
        vert_point += 1
        horiz_point = 1
    return output

hours_dict = fortnight_processor(fortnight)

def pay_calc(hours_dict, name):
    rate_base = 20.4756
    extra_afternoon = 19.2200
    modifier_weekend = 0.50
    modifier_casual = 1.25

    data = hours_dict[name]
    print(data)

    total_base = 0.0
    total_extras = 0.0

    for shift in data:
        start = int(shift[0])
        finish = int(shift[1])
        hours = (finish - start)/100.0
        # Subtracting lunchbreak
        if(hours > 6):
            print("subtracting lunchbreak")
            hours -= 0.5
        print(hours)
        # Remember that only the base rate is mutlipled by the casual
        # modifier. The other amounts are extras.
        total_base += hours * rate_base
        # Checking for afternoon .
        if(finish > 1800):
            print("adding afternoon extra")
            total_extras += extra_afternoon
        # Checking for weekend.
        if(shift[2] == True):
            print("multiplying by weekend modifier")
            total_extras += hours * rate_base * modifier_weekend
        # Checking for evening weekend (for no meal break extra).
        if (finish > 1800 and shift[2] == True):
            total_extras += extra_afternoon
        print("base:    " + str(total_base))
        print("extras : " + str(total_extras))

    return total_base * modifier_casual + total_extras

print(pay_calc(hours_dict, name))






#space
