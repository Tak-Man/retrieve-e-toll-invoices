# retrieve-e-toll-invoices
A semi-automatic solution for retrieving e-toll invoices from sanral.co.za. No API exists for this use currently.
This solution was developed to assist people with a large number of e-toll accounts - too large to practically page through manually.

An account with a password is still required for this solution to work.

The following files should be included in this directory:
- data_manipulation.py
- get_credit_notes.py
- get_invoices.py
- tools.py

The entry points are:
- get_credit_notes.py
- get_invoices.py

Please note that in the development of this solution many errors were encountered with retrieving data. So the timing of the program was slowed down a lot. This was done by adding explicit waiting in the program.

