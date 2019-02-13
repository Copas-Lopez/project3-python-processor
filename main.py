from urllib2 import urlopen
import re
from datetime import datetime
import sys
from operator import itemgetter
import heapq
import collections
import os
import time


def least_common_values(array, to_find=None):
    counter = collections.Counter(array)
    if to_find is None:
        return sorted(counter.items(), key=itemgetter(1), reverse=False)
    return heapq.nsmallest(to_find, counter.items(), key=itemgetter(1))

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


#Apache Webserver format:
#%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\
regex = '(.*?) - (.*) \[(.*?)\] (.*?) (\d+) (.)'

print('GETTING FILE...')
#Get log from link
url = "https://s3.amazonaws.com/tcmg476/http_access_log"
response = urlopen(url)
log = unicode(log, "utf-8")
print("COMPLETE")
time.sleep(1)
cls()

#Split log into lines for easier parsing
lines = log.splitlines()

total_requests = len(lines)
total_malformed = 0
total_client_errors = 0
total_redirects = 0

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

file_names = []

day_requests = []
week_requests = []
month_requests = []

print('PARSING DATA...')

last_day = 0
week_total = 0
requests_day = 0

#Main loop
for i in tqdm(range(len(lines))):
    match = re.match(regex,lines[i])
    if match:
        #Split the line apart for each section
        curr_line = list(match.groups())

        #Date parsing
        date = curr_line[2].strip('[').split(':')[0]
        formated_date = datetime.strptime(date, '%d/%b/%Y')
        file_months[formated_date.month - 1].append(lines[i])
        if formated_date.weekday() == last_day:
            requests_day = requests_day + 1
            week_total = week_total + 1
        else:
            day_requests.append(requests_day)
            requests_day = 1
            last_day = formated_date.weekday()
            if formated_date.weekday() == 0:
                week_requests.append(week_total)
                week_total = 0
        #Status Code
        code = list(curr_line[4])
        if code[0] is '4':
            total_client_errors = total_client_errors + 1
        elif code[0] is '3':
            total_redirects = total_redirects + 1

        #Files
        request = curr_line[3].split(' ')
        file_names.append(request[1])

    else:
        #ALL malformed requests are ignored
        total_malformed = total_malformed + 1
cls()
print('WRITING MONTHLY FILES...')
for i in tqdm(range(len(file_months))):
    string_name = "./month_text/" + month_names[i] + ".txt"
    month_file = open(string_name, "a")
    for d in tqdm(range(len(file_months[i]))):
        month_file.write(file_months[i][d] + "\n")
    month_file.close
    month_requests.append(len(file_months[i]))
cls()
c = collections.Counter(file_names).most_common()[-1]
print('==== Statistics ====')
print('Total Requests:: ' + str(total_requests))
print('Total Malformed Requests:: ' + str(total_malformed) + ' - ' + str(round(((total_malformed / total_requests)*100),2)) + '%')
print('Total Client Errors:: ' + str(total_client_errors) + ' - ' + str(round(((total_client_errors / total_requests)*100),2)) + '%')
print('Total Redirects:: ' + str(total_redirects) + ' - ' + str(round(((total_redirects / total_requests)*100),2)) + '%')
print('Average Requests Made Per Day:: ' + str(round(statistics.mean(day_requests))))
print('Average Requests Made Per Week:: ' + str(round(statistics.mean(week_requests))))
print('Average Requests Made Per Month:: ' + str(round(statistics.mean(month_requests))))
print('Most Common File:: ' + statistics.mode(file_names))
print('Least Common File:: ' + str(c[0]))
