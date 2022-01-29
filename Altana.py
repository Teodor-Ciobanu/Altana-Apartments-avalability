import requests
from bs4 import BeautifulSoup
import concurrent.futures

def get_ap_info(a):
    message = ''
    ap = a.find('span', class_ = 'sr-only')
    if ap != None:
        number = ap.text.strip().split(' ')[-1]
        #if number != '' and number != 'Number':
            #print(number)
    button = a.find('button', class_ = 'btn btn-primary')
    if button != None:
        onclick = button.get('onclick')
        # print(onclick)
        moveInDate = onclick.split('MoveInDate=')[-1].strip("'")
        message += str(number + ',  Move In Date ' + moveInDate + '\n')
        # print(number, ',  Move In Date ', moveInDate)
    return message

def get_plan(plan):
    message = ''
    itemName = plan.find('h2', class_ = 'card-title h4 font-weight-bold text-capitalize').text.strip()
    itemAva = plan.find('span', class_ = 'd-block mb-2 font-weight-bold').text.strip()
    itemInfo = plan.find_all('div', class_ = 'd-flex align-items-center')    
    if 'Available' in itemAva:
        planN = plan.find('div', class_="row")
        link = planN.find_all(lambda tag: tag.name == 'a' and tag.get('href') )[0].get('href')
        link = url + '/' + link.split('/')[-1]        
        info = ', '.join([i.text.strip() for i in itemInfo])
        message += str(itemName + ', ' + itemAva + '\n' + info + '\n')
        r = requests.get(link)
        s = BeautifulSoup(r.content, 'lxml')
        aps = s.find_all('div', class_ = 'card')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(get_ap_info, aps)
            for result in results:
                message += result

        message += '\n'
    return message

url = 'https://www.altanaglendale.com/floorplans'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')
plans = soup.find_all('div', class_ = 'card text-center h-100')
message = ''

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(get_plan, plans)
    for result in results:
        message += result

import ctypes 
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
Mbox('Altana Apartments Available', message, 0)
#print(message)

"""
cmd auto-py-to-exe
"""