import tools
import pandas as pd
import numpy as np
import os
import datetime
from openpyxl import load_workbook

destination_folder = "../retrieve-e-toll-invoices-data/output/"
source_folder = "../retrieve-e-toll-invoices-data/archive/"
data_details_df = tools.read_pickles_from_folder(source_folder, startswith="details_table")
data_invoices_df = tools.read_pickles_from_folder(source_folder, startswith="invoices_table")

print("data_invoices_df :")
print(data_invoices_df.head(10))
print("data_invoices_df.shape :", data_invoices_df.shape)

discounted_balance_total = data_invoices_df["Discounted Balance"].sum()
print("discounted_balance_total :", discounted_balance_total)
amount_due_total = data_invoices_df["Amount Due"].sum()
print("amount_due_total :", amount_due_total)


print("data_details_df :")
print(data_details_df.head(10))
print("data_details_df.shape :", data_details_df.shape)

amount_including_vat_total = data_details_df["Amount Incl VAT"].sum()
print("amount_including_vat_total :", amount_including_vat_total)

summarized_data_details_df = data_details_df.groupby(by=["Document Number"])["Amount Incl VAT"].sum()
print("summarized_data_details_df :")
print(summarized_data_details_df)


notes_df = tools.read_pickles_from_folder(source_folder, startswith="credit_notes_table_pages")
print("notes_df :")
print(notes_df.head(10))
print("notes_df.shape :", notes_df.shape)
notes_total_amount_due = notes_df["Amount Due"].sum()
print("notes_total_amount_due :", notes_total_amount_due)

notes_details_df = tools.read_pickles_from_folder(source_folder, startswith="credit_notes_details_table_pages")
print("notes_details_df :")
print(notes_details_df.head(10))
print("notes_details_df.shape :", notes_details_df.shape)
notes_details_amount_excl_vat = notes_details_df["Amount Excl VAT"].sum()
notes_details_amount_incl_vat = notes_details_df["Amount Incl VAT"].sum()
print("notes_details_amount_excl_vat :", notes_details_amount_excl_vat)
print("notes_details_amount_incl_vat :", notes_details_amount_incl_vat)

pivoted_notes_df = pd.pivot_table(notes_df, values="Amount Due", index=["Number"], columns=["Document Type"],
                                  aggfunc=np.sum)
print("pivoted_notes_df: ")
print(pivoted_notes_df.head())
print("pivoted_notes_df.shape :", pivoted_notes_df.shape)
print()

combined_df = data_invoices_df[["Vehicle Licence Plate Number (VLN)", "Number", "Date",
                                "Amount Due", "Discounted Balance"]]\
                .merge(summarized_data_details_df,
                       left_on=["Number"],
                       right_on=["Document Number"],
                       how="left")
combined_df["Difference"] = round(combined_df["Amount Due"], 2) - round(combined_df["Amount Incl VAT"], 2)
combined_df.columns = ["VLN", "Document Number", "Invoice Date", "Invoice-Amount Due", "Invoice-Discounted Balance",
                       "Details-Amount Incl VAT", "Difference"]
combined_df = combined_df.fillna(0.00)
print("combined_df :")
print(combined_df.head())

time_now = datetime.datetime.now()
output_file_name = os.path.join(destination_folder, "e_toll_summary_" + time_now.strftime("%Y_%m_%d_%H_%M_%S") + ".xlsx")
# writer = pd.ExcelWriter(output_file_name, engine='xlsxwriter')
combined_df.to_excel(output_file_name, sheet_name='Summary', index=False)
book = load_workbook(output_file_name)
writer = pd.ExcelWriter(output_file_name, engine='openpyxl')
writer.book = book
data_invoices_df.to_excel(writer, sheet_name='Invoices', index=False)
data_details_df.to_excel(writer, sheet_name='Invoice_Details', index=False)
notes_df.to_excel(writer, sheet_name='Notes', index=False)
notes_details_df.to_excel(writer, sheet_name='Notes_Details', index=False)
writer.save()
writer.close()


