from urllib.request import urlopen
from datetime import datetime
from tqdm import tqdm
from time import sleep

#Get log from link
url = "https://s3.amazonaws.com/tcmg476/http_access_log"
response = urlopen(url)
log = str(response.read(), "utf-8")

#Create and write contents to text file
text_file = open("Output.txt", "w")
text_file.write(log[0:71])
text_file.close()

#Split log into lines for easier parsing
test = log.splitlines()
lines = test


#Setting base variables for all our counting
days = []
months = []
years = []
total_unknowns = 0
redirects = 0
files = []

Jan = []
Feb = []
Mar = []
Apr = []
May = []
Jun = []
Jul = []
Aug = []
Sep = []
Oct = []
Nov = []
Dec = []
file_months = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

#Main loop to go through each line
for i in tqdm(range(len(lines))):

    #==== REQUIREMENT 1 ====#
    total_request = len(lines)
    curr_line = lines[i]
    #print(curr_line)

    #Split the line
    split = curr_line.split(" ")

    #Special case checking format of line
    if len(split) < 8:
        continue

    next = list(split[2])
    #print(next)
    if next[0] is "[":
        date_time = split[2].strip("[").split(":")
        date = date_time[0]
        date = datetime.strptime(date, "%d/%b/%Y")

        #Add line into month matrix
        file_months[date.month - 1].append(curr_line)
    else:
        date_time = split[3].strip("[").split(":")
        date = date_time[0]
        date = datetime.strptime(date, "%d/%b/%Y")

        #Add line into month matrix
        file_months[date.month - 1].append(curr_line)

    #Get Percentages

    if len(split) < 9:
        continue
    else:
        #Split codes
        code = split[8].split()
        #Check for 404
        if code[0] == "4":
            total_unknowns = total_unknowns+1
        elif code[0] == "3":
            redirects = redirects+1

            #Get files
            files.append(split[6])

    pass

for i in range(len(file_months)):
    string_name = "./month_text/" + month_names[i] + ".txt"
    month_file = open(string_name, "a")
    for d in range(len(file_months[i])):
        month_file.write(file_months[i][d] + "\n")
    month_file.close
##Write to monthly files
#string_name = "./month_text/" + file_months[date.month - 1] + ".txt"
#month_file = open(string_name, "a")
#month_file.write(curr_line + "\n")
#month_file.close()
