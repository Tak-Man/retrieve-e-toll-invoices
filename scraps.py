# invoices_table_0 = pd.DataFrame(columns=table_headers)
# print("invoices_table_0 :")
# print(invoices_table_0)
# retries = 3
# failed = False
# for i in range(0, 3):
# # for i in range(0, number_pages):
#     no_records_start, _ = invoices_table_0.shape
#     soup = BeautifulSoup(driver.page_source, 'lxml')
#     # print(soup)
#     table_footer_next_button = WebDriverWait(driver, 120)\
#         .until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]')))
#
#     current_try = 0
#     while True:
#         table_rows = tools.get_info_from_one_table_0(soup=soup, driver=driver, table_id=table_id, table_headers=table_headers)
#         # print("table_rows :")
#         # print(table_rows)
#
#         temp_df = pd.DataFrame(table_rows)
#         # print("temp_df :")
#         # print(temp_df)
#         invoices_table_0 = invoices_table_0.append(temp_df)
#         invoices_table_0.drop_duplicates(inplace=True)
#         no_records_end, _ = invoices_table_0.shape
#         current_try += 1
#         if current_try >= retries:
#             print("Could not get new data after {} retries.".format(retries))
#             failed = True
#             break
#         if no_records_end <= no_records_start:
#             print("Could not get new data, trying again...")
#             time.sleep(2)
#         else:
#             print("Got new data.")
#             break
#
#     if failed:
#         break
#     # test_button = driver.find_element_by_xpath('//*[@id="ctl00_MainContentHolder_DocumentListControl1_grdDocuments_ctl00"]/tfoot/tr/td/table/tbody/tr/td/div[3]/input[1]')
#     # if len(test_button) < 1:
#     #     print("No more pages left.")
#     #     break
#
#     print("Element is visible? " + str(table_footer_next_button.is_displayed()))
#     driver.implicitly_wait(10)
#     ActionChains(driver).move_to_element(table_footer_next_button).click(table_footer_next_button).perform()
#     # table_footer_next_button.click()
#     # driver.refresh()
#     driver.implicitly_wait(10)
#     time.sleep(5)
#
# invoices_table_0.reset_index(drop=True, inplace=True)
# print("invoices_table_0.shape :", invoices_table_0.shape)
# print("invoices_table_0 :")
# print(invoices_table_0)