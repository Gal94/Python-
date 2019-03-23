'''
This file will contain all the scrapers scripts I use for in the Clever bot
Data goes into data bases.
Things to add:
        1) Add user stats
        2) Fix the get_inactive query to check if user is not maxed
        3) More tables and queries


    STARTED ADDING SQLITE SUPPORT
'''

import sql
from bs4 import BeautifulSoup
import csv
import requests
import time
import psutil
import datetime


def fix_date(last_xp):
    '''
    Fixes Date to DD/MM/YY, and subtracts today's date from last inactive to find total inactivity time in months
    '''
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
              'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12, }

    today = datetime.date.today()
    last_xp = last_xp[18::].split(' ')
    last_xp[0] = last_xp[0][:len(last_xp[0])-2:]
    last_xp[1] = months[last_xp[1]]

    time_inactive = datetime.date(year=int(last_xp[2])+2000, month=int(last_xp[1]), day=int(last_xp[0]))
    inactive_time = (today - time_inactive)/30
    months_inactive = int(str(inactive_time)[0:2:])

    last_xp = str(last_xp).replace("'",'')
    last_xp = last_xp.replace(",", '')
    last_xp = last_xp.replace(" ", '-')

    return last_xp, months_inactive


def add_users():
    '''
    Adds user stats to into 2 tables
    '''


def isMaxed(rsn):
    rsn = rsn.replace(' ', '+')
    url = requests.get('http://www.runeclan.com/user/{}'.format(rsn)).text
    user_xp = BeautifulSoup(url, 'lxml').find('td', class_='xp_tracker_cxp').text
    print(psutil.virtual_memory())
    if user_xp == '5,400,000,000':
        return True
    else:
        return False
#'''

def inactive(months=1):
    '''
    :param months:
    :return: Detailed CSV file with the inactive members details. Inactivity duration depends on the months given
    '''
    t = time.time()

    try:
        sql.create_inactives()
    except Exception:
        sql.delete_inactives()
        sql.create_inactives()


    #Will scrape all pages CHECK 0 IS NOT BEING PASSED IN
    if months is not 1 and months is not 0:
        site = requests.get('http://www.runeclan.com/clan/Clever/members?inactivity={}-months'.format(months)).text
    else:
        site = requests.get('http://www.runeclan.com/clan/Clever/members?inactivity={}-month'.format(months)).text

    scrap_info = BeautifulSoup(site, 'lxml')

    links_list = scrap_info.find_all('a')
    links_len = len(links_list)

    num_of_pages = links_list[links_len - 8: links_len - 7:]
    num_of_pages = str(num_of_pages)[31:33:].split('?')

    try:
    ##convert len of pages to an int
        if len(num_of_pages) > 1:
            num_of_pages.pop(1)
            num_of_pages = int(str(num_of_pages)[2:3])
        else:
            num_of_pages = int(str(num_of_pages)[2:4])
    except ValueError:
        num_of_pages = 1

    #with open('Inactives.csv', 'w') as csv_file:
        #csv_writer = csv.writer(csv_file)
        #csv_writer.writerow(['RSN', 'Joined clan', 'Last XP gain', 'rank', 'Clan XP'])
    for number in range(0, num_of_pages):

        if months is not 1 and months is not 0:
            url = requests.get('http://www.runeclan.com/clan/Clever/members/{}?inactivity={}-months'.format(number+1, months)).text
        elif months is 0:
            url = requests.get('http://www.runeclan.com/clan/Clever/members/{}?inactivity='.format(number+1)).text
        else:
            url = requests.get('http://www.runeclan.com/clan/Clever/members/{}?inactivity={}-month'.format(number+1, months)).text

        for user in BeautifulSoup(url, 'lxml').find_all('table', class_='regular')[1].find_all('tr')[1::]:

            rsn = user.find('a').text
            #if isMaxed(rsn) is False:
            join_date = user.find_all('span')[1].text
            index_slice = (str(join_date).find('L'))
            join_date = join_date[0:index_slice:]
            try:
                last_xp = user.find_all('span')[2].text
            except IndexError:
                last_xp = 'ACTIVE USER'

            if last_xp is not 'ACTIVE USER':
                last_xp, months_inactive = fix_date(last_xp)
                last_xp = last_xp[1:len(last_xp) - 1:]
            else:
                months_inactive = 0
                last_xp = last_xp[0:len(last_xp) - 1:]


            rank = user.find('td', class_='clan_td clan_rank').text

            clan_xp = user.find('td', class_='clan_td clan_xpgain').text

            sql.add_inactive(rsn, join_date, last_xp, rank, clan_xp, months_inactive)
                #csv_writer.writerow([rsn, join_date, last_xp, rank, clan_xp])
    #            else:
     #               continue
    print(time.time()-t)


if __name__ == '__main__':

    inactive()
    t1 = time.time()
    amount = sql.get_inactives(4)
    for user in amount:
        print(user)
    #print(amount)
    t2 = time.time()
    print(t2-t1)
