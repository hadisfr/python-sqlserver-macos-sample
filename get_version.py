#!/usr/bin/env python3

import locale

import pyodbc

server = '192.168.99.100'  # docker-machine ip
username = 'sa'
password = 'yourStrong(!)Password'

locale.setlocale(locale.LC_CTYPE, "C")
# https://github.com/Microsoft/homebrew-mssql-release/issues/18#issuecomment-397420786

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';PORT=1443' + ';UID=' + username + ';PWD=' + password)
cursor = cnxn.cursor()
cursor.execute('select @@VERSION;')
print(cursor.fetchone())
