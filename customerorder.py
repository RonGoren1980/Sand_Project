import requests
from bs4 import BeautifulSoup
import urllib
import pyodbc
from datetime import datetime
from xml.dom.minidom import parse, parseString
import time

a = open("C:\pyrun\out.txt")
Token = (a.read())


def get_data_from_sql():
    '''
    This part of the code, gets t
    :return:
    '''

    query = '''select * from CustomerOrder_XML'''
    conn = pyodbc.connect('Driver={SQL Server};''Server=S-BI;''Database=Shilav_DWH;''Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute(query)
    data = ''
    for row in cursor:
        data = row[0]
    return data


data = get_data_from_sql()

# time.sleep(60)

dom = parseString(data)
list_of_items = dom.getElementsByTagName('DATA')


# for item in list_of_items:
#     formatted_xml_item = item.toprettyxml(indent="  ")

def chunks(your_list, cut_on):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(your_list), cut_on):
        yield your_list[i:i + cut_on]


new_fixed_list = chunks(list_of_items, 10)

# Fixing the items in the chuncks
for chunk in new_fixed_list:  # Loading chunk
    items_list = []  # Creating empty list
    for item in chunk:  # Fixing items in chunk
        item = item.toprettyxml(indent="  ")
        items_list.append(item)  # adding items into items list

    # At this point, the items list is full.
    items_list_as_data = "".join(i for i in items_list)

    template = f"""=<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<DATACOLLECTION>
	<TransactionSet>1111</TransactionSet>
	{items_list_as_data}</DATACOLLECTION>""".encode('utf-8')

    # At this point, we want to send the template as a data object to the server
    url = "https://www.logtmspod.co.il/APIWebServiceTest/api/import/Outbound "
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;UTF-8',
        'Cookie': 'GCLB=CLeXxbmIlMeNbA',
        'User-Agent': 'PostmanRuntime/7.26.8',
        'AuthToken': Token
    }

    response = requests.request('POST', url, headers=headers, data=template)
    if '<CODE>100</CODE>' in response.text:
        print(f'------ERROR CODE: 100\n{response.text}\n------TEMPLATE:\n{template}\n------')
        file = open("error.txt", "w")
        try:
            template_err = parseString(template)
            template_err = template_err.toprettyxml(indent="  ")
            file.write(template_err)
            file.close()
        except Exception as e:
            print(e)
    else:
        print(f'[{response.status_code}] | {datetime.now()} | {len(template)} | {response.text}')
