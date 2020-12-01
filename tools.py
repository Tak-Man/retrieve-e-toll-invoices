import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import time
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def parse_table_footer(raw_text):
    reg_exp = r"([0-9]*) items in ([0-9]*) pages"
    result = re.findall(reg_exp, raw_text, re.IGNORECASE)
    result_dict = dict({"items": int(result[0][0]), "pages": int(result[0][1])})
    return result_dict


def get_table_num_items_pages(soup, table_id):
    document_list_table = soup.find("table", {"id": table_id})
    table_footer_text = document_list_table.find("tfoot").getText()
    # print("table_footer_text :", table_footer_text)

    items_pages = parse_table_footer(raw_text=table_footer_text)
    # print("items_pages :", items_pages)

    return items_pages


def get_table_headers_from_table(soup, table_id):
    document_list_table = soup.find("table", {"id": table_id})
    table_header = document_list_table.find("thead")
    # print("table_header :")
    # print(table_header)

    table_header_rows = table_header.find_all("tr")[0].find_all("th", {"scope": "col", "class": "rgHeader"})
    # print("table_header_rows :")
    # print(table_header_rows)

    table_headers = []
    for th in table_header_rows:
        table_headers.append(th.getText())

    return table_headers


def reset_table(table_id, driver, no_retries=3, wait_time=2, driver_wait=160):
    for i in range(0, no_retries):
        try:
            time.sleep(wait_time)
            x_path_first_page = \
                '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[1]/input[1]'
            # first_page = WebDriverWait(driver, driver_wait) \
            #     .until(EC.visibility_of_element_located((By.XPATH, x_path_first_page)))
            first_page = WebDriverWait(driver, driver_wait) \
                .until(EC.element_to_be_clickable((By.XPATH, x_path_first_page)))
            first_page.click()
            print("Reset table...")
            return True
        except:
            print("Could not reset table...")
            print("Trying again...")
            continue
    return False


def get_next_ten_pages(table_id, driver, next_type="first_ten", no_retries=3,
                       wait_time=2, driver_wait=160):
    if next_type == "first_ten":
        # Only 10 are displayed on each page
        x_path_next_ten_pages = \
            '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[11]'
        message = "Paged past first ten pages."
    elif next_type == "second_ten":
        x_path_next_ten_pages = \
            '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[12]'
        message = "Paged past second ten pages."

    for i in range(0, no_retries):
        try:
            time.sleep(wait_time * 3)
            next_ten_pages = WebDriverWait(driver, driver_wait) \
                .until(EC.visibility_of_element_located((By.XPATH, x_path_next_ten_pages)))
            # next_ten_pages = WebDriverWait(driver, driver_wait) \
            #     .until(EC.element_to_be_clickable((By.XPATH, x_path_next_ten_pages)))
            # next_ten_pages = WebDriverWait(driver, driver_wait) \
            #     .until(EC.presence_of_element_located((By.XPATH, x_path_next_ten_pages)))
            next_ten_pages.click()
            print(message)
            return True
        except:
            print("Could not get next ten pages...")
            print("Trying again...")
            continue
    return False


def goto_page_number(table_id, page_number, driver, no_retries=3, wait_time=2, driver_wait=160):
    for i in range(0, no_retries):
        try:
            time.sleep(wait_time * 2)
            x_path_current_page_1 = \
                '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[' \
                + str(page_number) + ']/span'
            # current_page_1 = WebDriverWait(driver, driver_wait) \
            #     .until(EC.visibility_of_element_located((By.XPATH, x_path_current_page_1)))
            current_page_1 = WebDriverWait(driver, driver_wait) \
                .until(EC.presence_of_element_located((By.XPATH, x_path_current_page_1)))
            current_page_1.click()
            # print("Went to adj page number {}.".format(page_number))
            return True
        except:
            print("Could not go to page ")
            print("Trying again...")
            continue
    return False


def get_info_from_table_0(soup, table_id, table_headers, tr_identifier):
    document_list_table = soup.find("table", {"id": table_id})

    table_headers_alt = table_headers.copy()
    table_headers_alt.append("tr_id")
    # print("table_headers_alt :", table_headers_alt)
    table_rows = []
    tr_ids = []
    for row in document_list_table.findAll("tr", id=lambda x: x and x.startswith(tr_identifier)):
        tr_id = row.get("id")
        # print("tr_id :", tr_id)
        tr_ids.append(tr_id)
        row_table_data = row.find_all("td")
        row_items = []
        for item in row_table_data:
            # print("item :", item)
            try:
                temp_text = item.getText()
            except:
                temp_text = "<BLANK>"
            row_items.append(temp_text)

        row_items.append(tr_id)
        # print("row_items :", row_items)
        temp_dict = {table_headers_alt[i]: row_items[i] for i in range(len(table_headers_alt))}
        table_rows.append(temp_dict)

    # print("table_rows :")
    # print(table_rows)
    # print("len(table_rows) :", len(table_rows))
    return table_rows, tr_ids


def get_info_from_table_1(driver, table_row_id, retries=5, wait_time=5, driver_wait=160):
    x_path = '//*[@id="' + table_row_id + '"]/td[1]/a'

    for i in range(retries):
        try:
            time.sleep(wait_time * 4)
            # link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, x_path)))
            link = WebDriverWait(driver, driver_wait).until(EC.visibility_of_element_located((By.XPATH, x_path)))  # .get_attribute("href")
            # print("Got link. Is is of type-{}".format(type(link)))
            link.click()
        except KeyError as e:
            print("Could not get link...")
            print("Trying again...")
            time.sleep(wait_time)
        break

    back_button = WebDriverWait(driver, driver_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="MainContentHolder_imgBtnBack"]')))#.get_attribute('href')

    soup = BeautifulSoup(driver.page_source, 'lxml')

    document_number = soup.find("input", {"id": "ctl00_MainContentHolder_documentDetailsView_txtDocumentNumber_text"})\
        .get("value")
    document_status = soup.find("input", {"id": "ctl00_MainContentHolder_documentDetailsView_txtDocumentStatus_text"})\
        .get("value")

    table_id = "ctl00_MainContentHolder_documentTransactions_RadGridDocTransactions_ctl00"
    tr_identifier = "ctl00_MainContentHolder_documentTransactions_RadGridDocTransactions_ctl00_"
    table_headers = get_table_headers_from_table(soup=soup, table_id=table_id)
    table_rows_df = pd.DataFrame(columns=table_headers)
    no_records_start, _ = table_rows_df.shape
    current_try = 0

    while True:
        table_rows, _ = get_info_from_table_0(soup=soup,
                                              table_id=table_id,
                                              table_headers=table_headers,
                                              tr_identifier=tr_identifier)

        temp_df = pd.DataFrame(table_rows)
        table_rows_df = table_rows_df.append(temp_df)
        table_rows_df.drop_duplicates(inplace=True)
        no_records_end, _ = table_rows_df.shape
        current_try += 1
        if current_try >= retries:
            print("Could not get new data after {} retries.".format(retries))
            return -1
        if no_records_end <= no_records_start:
            print("Could not get new data, trying again...")
            time.sleep(wait_time)
        else:
            print("Got new details.")
            break

    table_rows_df.reset_index(drop=True, inplace=True)

    table_rows_df["Document Number"] = document_number
    table_rows_df["Document Status"] = document_status

    # print("table_rows_df :")
    # print(table_rows_df)
    return table_rows_df, back_button


def get_info_from_table_0_s(soup, driver, table_id, tr_identifier, table_headers=None, get_table_next_level=False, retries=3,
                            number_pages=3, wait_time=5, driver_wait=160):
    if not table_headers:
        table_headers = get_table_headers_from_table(soup=soup, table_id=table_id)

        if table_id == "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00":
            table_headers[-4:] = ["Print", "e-mail", "Query", "Pay"]

    invoices_table_0 = pd.DataFrame(columns=table_headers)

    failed = False
    for i in range(0, number_pages):
        # for i in range(0, number_pages):
        no_records_start, _ = invoices_table_0.shape
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup)
        table_footer_next_button = WebDriverWait(driver, driver_wait) \
            .until(EC.element_to_be_clickable((By.XPATH,
            '//*[@id="ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]')))

        current_try = 0
        while True:
            table_rows, _ = get_info_from_table_0(soup, table_id, table_headers, tr_identifier)
            # print("table_rows :")
            # print(table_rows)

            temp_df = pd.DataFrame(table_rows)
            # print("temp_df :")
            # print(temp_df)
            invoices_table_0 = invoices_table_0.append(temp_df)
            invoices_table_0.drop_duplicates(inplace=True)
            no_records_end, _ = invoices_table_0.shape
            current_try += 1
            if current_try >= retries:
                print("Could not get new data after {} retries.".format(retries))
                failed = True
                break
            if no_records_end <= no_records_start:
                print("Could not get new data, trying again...")
                time.sleep(wait_time)
            else:
                print("Got new data.")
                break

        if failed:
            break
        # test_button = driver.find_element_by_xpath('//*[@id="ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]')
        # if len(test_button) < 1:
        #     print("No more pages left.")
        #     break

        print("Element is visible? " + str(table_footer_next_button.is_displayed()))
        # driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(table_footer_next_button).click(table_footer_next_button).perform()
        # table_footer_next_button.click()
        # driver.refresh()
        # driver.implicitly_wait(10)
        time.sleep(wait_time)

    invoices_table_0.reset_index(drop=True, inplace=True)
    print("invoices_table_0.shape :", invoices_table_0.shape)
    print("invoices_table_0 :")
    print(invoices_table_0)

    return invoices_table_0


def get_info_from_table_1_s(soup, driver, table_id, tr_identifier, table_headers=None, get_table_next_level=False,
                            retries=3,
                            number_pages=3, wait_time=5, driver_wait=160):
    if table_id == "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00":
        record_type = "invoices"
    elif table_id == "ctl00_MainContentHolder_CreditNoteListControl1_grdDocuments_ctl00":
        record_type = "credit notes"
    else:
        record_type = "<unkown>"

    if not table_headers:
        table_headers = get_table_headers_from_table(soup=soup, table_id=table_id)

        if table_id == "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00":
            table_headers[-4:] = ["Print", "e-mail", "Query", "Pay"]

    primary_df = pd.DataFrame(columns=table_headers)
    table_rows_dfs = []

    failed = False
    for i in range(0, number_pages):
        no_records_start, _ = primary_df.shape
        time.sleep(wait_time)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup)
        time.sleep(wait_time)

        x_path_current_page = '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[@class="rgCurrentPage"]'
        current_page = WebDriverWait(driver, driver_wait) \
            .until(EC.element_to_be_clickable((By.XPATH, x_path_current_page)))
        current_page_num = int(current_page.text)
        # print("current_page_num :", current_page_num)
        current_try = 0
        while True:
            table_rows, tr_ids = get_info_from_table_0(soup, table_id, table_headers, tr_identifier)

            temp_df = pd.DataFrame(table_rows)
            primary_df = primary_df.append(temp_df)
            primary_df.drop_duplicates(inplace=True)
            no_records_end, _ = primary_df.shape
            current_try += 1
            if current_try >= retries:
                print("Could not get new data after {} retries.".format(retries))
                failed = True
                break
            if no_records_end <= no_records_start:
                print("Could not get new data, trying again...try number {} of {}".format(current_try, retries))
                time.sleep(wait_time)
            else:
                print("Got new " + record_type + ".")
                for tr_id in tr_ids:
                    print("Getting details...")
                    table_rows_df, back_button = get_info_from_table_1(driver, table_row_id=tr_id,
                                                                       retries=5,
                                                                       wait_time=wait_time,
                                                                       driver_wait=driver_wait)
                    table_rows_dfs.append(table_rows_df)
                    back_button.click()
                    time.sleep(wait_time)
                    # Only 10 are displayed on each page
                    # Find the correct set of 10
                    if 10 < current_page_num:
                        x_path_next_ten_pages = \
                            '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[11]'
                        next_ten_pages = WebDriverWait(driver, driver_wait) \
                            .until(EC.visibility_of_element_located((By.XPATH, x_path_next_ten_pages)))
                        print("Got 'next_ten_pages'")
                        next_ten_pages.click()
                        time.sleep(wait_time)

                    if 20 < current_page_num:
                        num_tens_above_20 = int(current_page_num / 10) - 1
                        for iterator in range(0, num_tens_above_20):
                            x_path_next_ten_pages = \
                                '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[12]'
                            next_ten_pages = WebDriverWait(driver, driver_wait) \
                                .until(EC.visibility_of_element_located((By.XPATH, x_path_next_ten_pages)))
                            print("Got 'next_ten_pages'")
                            next_ten_pages.click()
                            time.sleep(wait_time)

                    # Find the correct page within the ten
                    if current_page_num % 10 != 1:
                        if 1 < current_page_num < 10:
                            current_page_num_adj = current_page_num
                        elif 10 < current_page_num:
                            if current_page_num % 10 == 0:
                                current_page_num_adj = 10 + 1
                            else:
                                remainder = (current_page_num % 10) + 1
                                current_page_num_adj = remainder

                        x_path_current_page_1 = \
                            '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[' \
                            + str(current_page_num_adj) + ']/span'
                        current_page_1 = WebDriverWait(driver, driver_wait) \
                            .until(EC.visibility_of_element_located((By.XPATH, x_path_current_page_1)))
                        current_page_1.click()
                        time.sleep(wait_time)

            break

        if failed:
            break

        x_path = '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]'
        table_footer_next_button = WebDriverWait(driver, driver_wait) \
            .until(EC.element_to_be_clickable((By.XPATH, x_path)))
        # driver.implicitly_wait(10)
        time.sleep(wait_time)
        ActionChains(driver).move_to_element(table_footer_next_button).click(table_footer_next_button).perform()
        # driver.implicitly_wait(10)
        time.sleep(wait_time)

    primary_df.reset_index(drop=True, inplace=True)

    details_df_cols = list(table_rows_dfs[0].columns)
    details_df = pd.DataFrame(columns=details_df_cols)

    for df in table_rows_dfs:
        details_df = details_df.append(df)

    details_df.reset_index(drop=True, inplace=True)

    return primary_df, details_df


def get_current_table_page_number(driver, table_id, no_retries=3, wait_time=3, driver_wait=160):
    for i in range(0, no_retries):
        try:
            wait_time_adj = wait_time * 3 # int(wait_time * 2)
            time.sleep(wait_time_adj)
            x_path_current_page = '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[@class="rgCurrentPage"]'
            current_page = WebDriverWait(driver, driver_wait) \
                .until(EC.presence_of_element_located((By.XPATH, x_path_current_page)))
            current_page_num = int(current_page.text)

            try:
                x_path_first_element = '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[1]'
                first_element = WebDriverWait(driver, driver_wait) \
                    .until(EC.presence_of_element_located((By.XPATH, x_path_first_element)))
                # print("Got 'first_element'...")
                first_element_num = int(first_element.text)

            except:
                first_element_num = -1
            # print("first_element_num :", first_element_num)

            x_path_second_element = '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[2]'
            second_element = WebDriverWait(driver, driver_wait) \
                .until(EC.presence_of_element_located((By.XPATH, x_path_second_element)))
            second_element_num = int(second_element.text)
            # print("second_element_num :", second_element_num)

            return current_page_num, first_element_num, second_element_num
        except:
            print("Could not get the current page number...")
            print("Trying again...")
            continue
    return False




def go_to_page(pages_number, driver, table_id, retries=3, number_of_pages_per_section=10,
               wait_time=5, driver_wait=160):
    print("Going to page {}".format(pages_number))
    current_page_num, first_element, second_element = \
        get_current_table_page_number(driver=driver, table_id=table_id,
                                      no_retries=3,
                                      wait_time=wait_time,
                                      driver_wait=driver_wait)
    # print("current_page_num :", current_page_num)
    # print("pages_number :", pages_number)
    if pages_number == current_page_num:
        print("Already on the required page.")
        return True # Already on the required page.

    try_number = 0

    while try_number < retries:
        # Reset table
        if current_page_num != 1:
            time.sleep(wait_time)
            print("Not on page 1. Resetting table...")
            reset_table_result = reset_table(table_id=table_id, driver=driver, no_retries=3, wait_time=wait_time,
                                             driver_wait=driver_wait)
            if not reset_table_result:
                try_number += 1
                continue

        if number_of_pages_per_section < pages_number:
            # print("Trying to get past first 10 pages...")
            get_first_ten_pages_result = get_next_ten_pages(table_id=table_id,
                                                            next_type="first_ten",
                                                            driver=driver,
                                                            no_retries=3,
                                                            wait_time=wait_time,
                                                            driver_wait=driver_wait)
            # print("get_first_ten_pages_result :", get_first_ten_pages_result)
            if not get_first_ten_pages_result:
                try_number += 1
                continue

        if (2 * number_of_pages_per_section) < pages_number:
            # print("Trying to get past second 10 pages...")
            num_tens_above_20 = int((pages_number-1) / 10) - 1
            for iterator in range(0, num_tens_above_20):
                get_second_ten_pages_result = get_next_ten_pages(table_id=table_id,
                                                                 next_type="second_ten",
                                                                 driver=driver,
                                                                 no_retries=3,
                                                                 wait_time=wait_time,
                                                                 driver_wait=driver_wait)
                # print("get_second_ten_pages_result :", get_second_ten_pages_result)
                if not get_second_ten_pages_result:
                    try_number += 1
                    continue

        # Find the correct page within the ten
        if pages_number % number_of_pages_per_section != 1:
            _, first_element, second_element = \
                get_current_table_page_number(driver=driver, table_id=table_id,
                                              no_retries=3,
                                              wait_time=wait_time,
                                              driver_wait=driver_wait)
            if (first_element == -1) and (second_element % number_of_pages_per_section != 1):
                # print("pages_number :", pages_number)
                # print("second_element :", second_element)
                end_stage_adj = second_element - (int(second_element / number_of_pages_per_section)
                                                  * number_of_pages_per_section + 1)
            else:
                end_stage_adj = 0
            # print("end_stage_adj :", end_stage_adj)
            if 1 < pages_number < (number_of_pages_per_section + 1):
                current_page_num_adj = pages_number
            elif number_of_pages_per_section < pages_number:
                if pages_number % number_of_pages_per_section == 0:
                    current_page_num_adj = number_of_pages_per_section + 1 # + end_stage_adj
                else:
                    current_page_num_adj = (pages_number % number_of_pages_per_section) + 1 + end_stage_adj
            # print("current_page_num_adj :", current_page_num_adj)

            goto_page_number_result = goto_page_number(table_id=table_id,
                                                       page_number=current_page_num_adj,
                                                       driver=driver,
                                                       no_retries=3,
                                                       wait_time=wait_time,
                                                       driver_wait=driver_wait)
            # print("goto_page_number_result", goto_page_number_result)
            if not goto_page_number_result:
                try_number += 1
                continue

        # else:
        #     current_page_num_adj = pages_number

        current_page_num_check, _, _ = \
            get_current_table_page_number(driver=driver,
                                          table_id=table_id,
                                          no_retries=3,
                                          wait_time=wait_time,
                                          driver_wait=driver_wait)
        # print("Check page number - {}. Looking for page - {}".format(current_page_num_check, pages_number))
        if pages_number == current_page_num_check:
            return True

        try_number += 1
    return False


def get_info_from_table_1_s_alt(soup, driver, table_id, tr_identifier, table_headers=None, get_table_next_level=False, retries=3,
                                number_pages=3, wait_time=5, driver_wait=160):
    if table_id == "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00":
        record_type = "invoices"
    elif table_id == "ctl00_MainContentHolder_CreditNoteListControl1_grdDocuments_ctl00":
        record_type = "credit notes"
    else:
        record_type = "<unkown>"

    if not table_headers:
        table_headers = get_table_headers_from_table(soup=soup, table_id=table_id)

        if table_id == "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00":
            table_headers[-4:] = ["Print", "e-mail", "Query", "Pay"]

    primary_df = pd.DataFrame(columns=table_headers)
    table_rows_dfs = []

    failed = False
    for i in range(0, number_pages):
        no_records_start, _ = primary_df.shape
        time.sleep(wait_time)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup)
        time.sleep(wait_time)

        x_path_current_page = '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[2]/a[@class="rgCurrentPage"]'
        current_page = WebDriverWait(driver, driver_wait) \
            .until(EC.element_to_be_clickable((By.XPATH, x_path_current_page)))
        current_page_num = int(current_page.text)
        # print("current_page_num :", current_page_num)
        current_try = 0
        while True:
            table_rows, tr_ids = get_info_from_table_0(soup, table_id, table_headers, tr_identifier)

            temp_df = pd.DataFrame(table_rows)
            primary_df = primary_df.append(temp_df)
            primary_df.drop_duplicates(inplace=True)
            no_records_end, _ = primary_df.shape
            current_try += 1
            if current_try >= retries:
                print("Could not get new data after {} retries.".format(retries))
                failed = True
                break
            if no_records_end <= no_records_start:
                print("Could not get new data, trying again...try number {} of {}".format(current_try, retries))
                time.sleep(wait_time)
            else:
                print("Got new " + record_type + ".")
                for tr_id in tr_ids:
                    print("Getting details...")
                    table_rows_df, back_button = get_info_from_table_1(driver, table_row_id=tr_id, retries=5,
                                                                       wait_time=wait_time, driver_wait=driver_wait)
                    table_rows_dfs.append(table_rows_df)
                    back_button.click()
                    time.sleep(wait_time)

                    go_to_page_result = go_to_page(pages_number=current_page_num, driver=driver, table_id=table_id,
                                                   retries=3, number_of_pages_per_section=10,
                                                   wait_time=wait_time, driver_wait=driver_wait)
                    # print("go_to_page_result :", go_to_page_result)
                    if go_to_page_result:
                        break

        if failed:
            break

        x_path = '//*[@id="' + table_id + '"]/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]'
        table_footer_next_button = WebDriverWait(driver, driver_wait) \
            .until(EC.element_to_be_clickable((By.XPATH, x_path)))
        # driver.implicitly_wait(10)
        time.sleep(wait_time)
        ActionChains(driver).move_to_element(table_footer_next_button).click(table_footer_next_button).perform()
        # driver.implicitly_wait(10)
        time.sleep(wait_time)

    primary_df.reset_index(drop=True, inplace=True)

    details_df_cols = list(table_rows_dfs[0].columns)
    details_df = pd.DataFrame(columns=details_df_cols)

    for df in table_rows_dfs:
        details_df = details_df.append(df)

    details_df.reset_index(drop=True, inplace=True)

    return primary_df, details_df


def get_info_from_pages(pages_numbers,
                        soup, driver, table_id, tr_identifier,
                        table_headers=None, retries=3, wait_time=5, driver_wait=160):
    if table_id == "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00":
        record_type = "invoices"
    elif table_id == "ctl00_MainContentHolder_CreditNoteListControl1_grdDocuments_ctl00":
        record_type = "credit notes"
    else:
        record_type = "<unkown>"

    if not table_headers:
        table_headers = get_table_headers_from_table(soup=soup, table_id=table_id)

        if table_id == "ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00":
            table_headers[-4:] = ["Print", "e-mail", "Query", "Pay"]

    primary_df = pd.DataFrame(columns=table_headers)
    table_rows_dfs = []

    # length_pages_numbers = len(pages_numbers)
    # pages_completed = 0
    for i in pages_numbers:
        # print("Executing <<go_to_page_result_init>>")
        go_to_page_result_init = go_to_page(pages_number=i, driver=driver, table_id=table_id,
                                            retries=3, number_of_pages_per_section=10,
                                            wait_time=wait_time, driver_wait=driver_wait)
        # print("go_to_page_result_init :", go_to_page_result_init)

        no_records_start, _ = primary_df.shape
        # time.sleep(wait_time * 3)

        # print(soup)

        current_try = 0
        while True:
            time.sleep(wait_time * 2)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            table_rows, tr_ids = get_info_from_table_0(soup, table_id, table_headers, tr_identifier)

            temp_df = pd.DataFrame(table_rows)
            primary_df = primary_df.append(temp_df)
            primary_df.drop_duplicates(inplace=True)
            no_records_end, _ = primary_df.shape
            current_try += 1
            if current_try >= retries:
                print("Could not get new data after {} retries.".format(retries))
                break
            if no_records_end <= no_records_start:
                print("Could not get new data, trying again...try number {} of {}".format(current_try, retries))
                time.sleep(wait_time)
            else:
                print("Got new " + record_type + ".")

            for tr_id in tr_ids:
                # print("Getting details...")
                table_rows_df, back_button = get_info_from_table_1(driver, table_row_id=tr_id, retries=5,
                                                                   wait_time=wait_time, driver_wait=driver_wait)
                table_rows_dfs.append(table_rows_df)
                back_button.click()
                time.sleep(wait_time)

                # print("Executing <<go_to_page_result>>")
                go_to_page_result = go_to_page(pages_number=i, driver=driver, table_id=table_id,
                                               retries=3, number_of_pages_per_section=10,
                                               wait_time=wait_time, driver_wait=driver_wait)
                # print("go_to_page_result :", go_to_page_result)
                if not go_to_page_result:
                    break
            break

    primary_df.reset_index(drop=True, inplace=True)

    details_df_cols = list(table_rows_dfs[0].columns)
    details_df = pd.DataFrame(columns=details_df_cols)

    for df in table_rows_dfs:
        details_df = details_df.append(df)

    details_df.reset_index(drop=True, inplace=True)

    return primary_df, details_df


def get_info_from_pages_into_dir(pages_numbers,
                                 destination_dir, destination_file_name_1, destination_file_name_2,
                                 soup, driver, table_id,
                                 tr_identifier,
                                 table_headers=None, retries=3, wait_time=5, driver_wait=160):

    try:
        primary_df, details_df = get_info_from_pages(pages_numbers=pages_numbers,
                                                     soup=soup,
                                                     driver=driver,
                                                     table_id=table_id,
                                                     tr_identifier=tr_identifier,
                                                     table_headers=table_headers,
                                                     retries=retries,
                                                     wait_time=wait_time,
                                                     driver_wait=driver_wait)

        # page_number_str = "_"
        if len(pages_numbers) > 1:
            page_number_str = "_pages_" + str(pages_numbers[0]) + "-" + str(pages_numbers[-1])
        else:
            page_number_str = "_pages_" + str(pages_numbers[0])

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        primary_df_table_name_1_csv = os.path.join(destination_dir, destination_file_name_1 + page_number_str + ".csv")
        primary_df_table_name_1_excel = os.path.join(destination_dir, destination_file_name_1 + page_number_str + ".xlsx")
        primary_df_table_name_2_csv = os.path.join(destination_dir, destination_file_name_2 + page_number_str + ".csv")
        primary_df_table_name_2_excel = os.path.join(destination_dir, destination_file_name_2 + page_number_str + ".xlsx")

        primary_df.to_csv(primary_df_table_name_1_csv, sep="|", index=False)
        primary_df.to_excel(primary_df_table_name_1_excel, sheet_name='Details', index=False)
        details_df.to_csv(primary_df_table_name_2_csv, sep="|", index=False)
        details_df.to_excel(primary_df_table_name_2_excel, sheet_name='Details', index=False)

        primary_df_table_name_1_pkl = os.path.join(destination_dir, destination_file_name_1 + page_number_str + ".pkl")
        primary_df_table_name_2_pkl = os.path.join(destination_dir, destination_file_name_2 + page_number_str + ".pkl")

        primary_df.to_pickle(primary_df_table_name_1_pkl)
        details_df.to_pickle(primary_df_table_name_2_pkl)

        return True

    except:
        return False


def read_pickles_from_folder(source_folder, startswith="details_table"):
    first_file = True
    return_df = None
    for test_file in os.listdir(source_folder):
        if test_file.endswith("pkl") and test_file.startswith(startswith):
            temp_df = pd.read_pickle(os.path.join(source_folder, test_file))
            if first_file:
                return_df = temp_df
            else:
                return_df = return_df.append(temp_df)
            first_file = False

    df_cols = list(return_df.columns)

    check_in_cols = ["amount", "balance", "vat"]
    for col in df_cols:
        # if any(ele in col.lower for ele in check_in_cols):
        if ("amount" in col.lower()) or ("balance" in col.lower()) or ("vat" in col.lower()):
            return_df[col] = return_df[col].apply(lambda x: x.replace("R ", ""))
            return_df[col] = return_df[col].apply(lambda x: x.replace(",", "."))
            return_df[col] = pd.to_numeric(return_df[col])

    drop_cols = ["Option", "Print", "e-mail", "Query", "Pay", "tr_id"]
    df_cols_adj = [x for x in df_cols if x not in drop_cols]

    return_df.drop_duplicates(inplace=True)
    return_df = return_df[df_cols_adj]
    return_df.reset_index(inplace=True, drop=True)
    return return_df

