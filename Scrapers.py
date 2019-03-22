'''
This file will contain all the scrapers scripts I use for in the Clever bot

Things to add:

  1)Remove maxed xp people from list - check each person for xp column (use an external function).

Optional - Change ranks from string to images.
'''

from bs4 import BeautifulSoup
import csv
import requests
import time


def inactive(months=3):
    '''
    :param months:
    :return: Detailed CSV file with the inactive members details. Inactivity duration depends on the months given
    '''
    t = time.time()
    if months is not 1 and months is not 0:
        site = requests.get('http://www.runeclan.com/clan/Clever/members?inactivity={}-months'.format(months)).text
    elif months is 0:
        site = requests.get('http://www.runeclan.com/clan/Clever/members?inactivity=').text
    else:
        site = requests.get('http://www.runeclan.com/clan/Clever/members?inactivity={}-month'.format(months)).text
    scrap_info = BeautifulSoup(site, 'lxml')

    links_list = scrap_info.find_all('a')
    links_len = len(links_list)
    print(links_len)

    num_of_pages = links_list[links_len - 8: links_len - 7:]
    num_of_pages = str(num_of_pages)[31:33:].split('?')

    try:
    ##convert len of pages to an int
        if len(num_of_pages) > 1:
            num_of_pages.pop(1) #clean garbage element
            num_of_pages = int(str(num_of_pages)[2:3])
        else:
            num_of_pages = int(str(num_of_pages)[2:4])
    except ValueError:
        num_of_pages = 1

    with open('Inactives.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['RSN', 'Joined clan', 'Last XP gain', 'rank', 'Clan XP'])
        for number in range(0, num_of_pages):

            if months is not 1 and months is not 0:
                url = requests.get('http://www.runeclan.com/clan/Clever/members/{}?inactivity={}-months'.format(number+1, months)).text
            elif months is 0:
                url = requests.get('http://www.runeclan.com/clan/Clever/members/{}?inactivity='.format(number+1)).text
            else:
                url = requests.get('http://www.runeclan.com/clan/Clever/members/{}?inactivity={}-month'.format(number+1, months)).text

            for user in BeautifulSoup(url, 'lxml').find_all('table', class_='regular')[1].find_all('tr')[1::]:

                rsn = user.find('a').text

                join_date = user.find_all('span')[1].text
                index_slice = (str(join_date).find('L'))
                join_date = join_date[0:index_slice:]
                try:
                    last_xp = user.find_all('span')[2].text
                except IndexError:
                    last_xp = 'ACTIVE USER'

                rank = user.find('td', class_='clan_td clan_rank').text

                clan_xp = user.find('td', class_='clan_td clan_xpgain').text

                csv_writer.writerow([rsn,join_date,last_xp,rank,clan_xp])

    print(time.time()-t)
if __name__ == '__main__':
    inactive(0)
