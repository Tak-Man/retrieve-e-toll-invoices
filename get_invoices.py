from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

import datetime
import tools

start_time = datetime.datetime.now()
print()
print("*" * 150)
print("Process started @", str(start_time))
print("*" * 150)

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(160)
driver.get("https://vpcweb.vpc.sanral.co.za/PublicWebSiteRoadUser/PersonAccountInfo.aspx")

login_button = driver.find_element_by_id("MainContentHolder_btnLogin")
print("Found 'Login' button...")
WebDriverWait(driver, timeout=600).until(EC.staleness_of(login_button))

active_documents = driver.find_element_by_id("MenuContentHolder_lnkActiveDocuments")
print("Found 'Active Documents' button...")
active_documents.click()

table_id = "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00"
tr_identifier = "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00_"
soup = BeautifulSoup(driver.page_source, 'lxml')
items_pages = tools.get_table_num_items_pages(soup=soup, table_id=table_id)
print("items_pages :", items_pages)
number_pages = items_pages["pages"]

table_headers = tools.get_table_headers_from_table(soup=soup, table_id=table_id)
table_headers[-4:] = ["Print", "e-mail", "Query", "Pay"]
print("table_headers :", table_headers)

# invoices_table = tools.get_info_from_table_0_s(soup=soup, driver=driver,
#                                                table_id=table_id,
#                                                tr_identifier=tr_identifier,
#                                                  table_headers=table_headers, get_table_next_level=False,
#                                                  retries=3, number_pages=2,
#                                                  wait_time=2, driver_wait=160)

# invoices_table, details_table = tools.get_info_from_table_1_s_alt(soup=soup, driver=driver,
#                                                                   table_id=table_id,
#                                                                   tr_identifier=tr_identifier,
#                                                                   table_headers=table_headers,
#                                                                   get_table_next_level=False,
#                                                                   retries=3, number_pages=12,
#                                                                   wait_time=2, driver_wait=160) # number_pages + 1

# invoices_table, details_table = tools.get_info_from_pages(pages_numbers=[1, 12],
#                                                           soup=soup,
#                                                           driver=driver,
#                                                           table_id=table_id,
#                                                           tr_identifier=tr_identifier,
#                                                           table_headers=table_headers,
#                                                           retries=3,
#                                                           wait_time=2, driver_wait=160)
#
# invoices_table.to_csv("../retrieve-e-toll-invoices-data/dumps/invoices_table.csv", sep="|")
# invoices_table.to_excel("../retrieve-e-toll-invoices-data/dumps/invoices_table.xlsx", sheet_name='Details')
# details_table.to_csv("../retrieve-e-toll-invoices-data/dumps/details_table.csv", sep="|")
# details_table.to_excel("../retrieve-e-toll-invoices-data/dumps/details_table.xlsx", sheet_name='Details')

page_numbers_list = []
destination_dir = "../retrieve-e-toll-invoices-data/dumps/"

# page_numbers_list.append([x for x in range(91, 100 + 1)])

for i in range(41, 100):
    page_numbers_list.append([x for x in range(i, i + 1)])

no_retries = 3
for page_numbers in page_numbers_list:
    try_number = 0
    while try_number < no_retries:
        print("page_numbers :", page_numbers)
        result = tools.get_info_from_pages_into_dir(pages_numbers=page_numbers,
                                                    destination_dir=destination_dir,
                                                    destination_file_name_1="invoices_table",
                                                    destination_file_name_2="details_table",
                                                    soup=soup,
                                                    driver=driver,
                                                    table_id=table_id,
                                                    tr_identifier=tr_identifier,
                                                    table_headers=table_headers,
                                                    retries=5,
                                                    wait_time=1,
                                                    driver_wait=160)
        print("Success = {}. After {} tries".format(result, try_number+1))
        if result:
            break
        else:
            print("Trying again. Try number - {}".format(try_number))
            try_number += 1

end_time = datetime.datetime.now()
duration = end_time - start_time
print()
print("*" * 150)
print("Process ended @", str(end_time))
print("Duration -", str(duration))
print("*" * 150)