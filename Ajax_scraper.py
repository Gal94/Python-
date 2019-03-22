'''
a Simple Web Scraper that scrapes AJAX injected text into a csv file.
To be added as a user command for a discord bot.

All the data that has been scraped here is for learning purposes only, this script is by no means affiliated
with Jagex ltd or Runescape.

**To do:

    Add code to log if operation was successful, amount of memory consumed and total time it took to
    execute the script.



Ver 0.0
'''
from bs4 import BeautifulSoup
import requests
import csv
import time as t


source_website = requests.get('http://jq.world60pengs.com/rest/cache/actives.json?_=1553060077619').text
scrap_info = BeautifulSoup(source_website, 'lxml').text[20:]

new_info_string = ''
for letter in scrap_info:
    if letter is not '"' and letter is not '{':
        new_info_string += letter

new_info = new_info_string.split(',')

data_list = []
for element in new_info:
    element = element.split(":")

    if element[0] == 'name' or element[0] == 'last_location' or element[0] == 'disguise'\
            or element[0] == 'time_seen' or element[0] == 'warning' or element[0] == 'requirements':
                data_list.append(element)

i = 1
info = []
data_list = data_list[:len(data_list)-1:]


with open('Penguins_locations.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Location', 'Last seen area', 'Hides in', 'Last report', 'Danger', 'Requirements'])

    while i <= len(data_list) :
        if data_list[i-1][1] is "":
            info.append("None")
        else:
            info.append(data_list[i-1][1])

        if i % 6 == 0:
            if info[i-1] != 'None':
                info[i-1] = info[i-1][10:len(info[i-1]) - 7:]

            try:
                epoch = int(info[i-3])
                if (int((t.time() - epoch)/60)) > 1:
                    minutes = str(int((t.time() - epoch)/60)) + ' Minutes ago'
                else:
                    minutes = 'Couple of seconds ago'
                csv_writer.writerow([info[i-6], info[i-5], info[i-4], minutes, info[i-2], info[i-1]])
            except IndexError:
                print(i)
        i += 1
