import pymysql
import mysql_config
sql_password = mysql_config.password
name = 'portfolio'

"""
Note: sql_password references my password in a separate file
"""

db = pymysql.connect("localhost","root",sql_password)
cursor = db.cursor()
query = 'DROP DATABASE IF EXISTS ' + name + ';'
cursor.execute(query)
query = "CREATE DATABASE IF NOT EXISTS " + name + ';'
cursor.execute(query)
query = "USE " + name + ';'
cursor.execute(query)

file = "portfolio.txt"
with open(file,'r') as f:
    line_count = 0
    stocks_set = set()
    for line in f:
        line = line.strip()

        if line_count == 0:
            headers = line.split(':')
            headers = [x.replace(' ','_') for x in headers]
            query1 = "DROP TABLE IF EXISTS stocks;"
            query2 = "DROP TABLE IF EXISTS holdings"
            cursor.execute(query1)
            cursor.execute(query2)
            query1 = "CREATE TABLE IF NOT EXISTS stocks ("
            query1 += headers[0] + " VARCHAR(10),"
            query1 += headers[1] + " VARCHAR(30));"
            query2 = "CREATE TABLE IF NOT EXISTS holdings ("
            query2 += headers[0] + " VARCHAR(10),"
            query2 += headers[2] + " DECIMAL(10,2),"
            query2 += headers[3] + " INT,"
            query2 += headers[4] + " DATE);"
            cursor.execute(query1)
            cursor.execute(query2)
            line_count += 1
            continue        
        data = line.split(':')
        stock_info = (data[0],data[1])
        stocks_set.add(stock_info)
        holdings_query = 'INSERT INTO holdings VALUES ("'
        holdings_query +=data[0] + '",'
        holdings_query +=data[2] + ','
        holdings_query +=data[3] + ',"'
        holdings_query +=data[4] + '");'
        cursor.execute(holdings_query)
for s_info in stocks_set:
    stock_query = 'INSERT INTO stocks VALUES ("'
    stock_query += s_info[0] + '","'
    stock_query += s_info[1] +'");'
    cursor.execute(stock_query)
db.commit()
db.close()

def get_price(ticker):
    import requests
    from bs4 import BeautifulSoup
    url = 'https://finance.google.com/finance?q='+ticker
    response = requests.get(url)
    try:
        results_page = BeautifulSoup(response.content,'lxml')
        price_raw = results_page.find('span', class_='pr').get_text()
        price = float(price_raw.strip("\n"))
    except:
        return None
    return price 

def get_pnl():
    import pymysql
    import mysql_config
    from decimal import Decimal
    
    ##Connecting to db
    sql_password = mysql_config.password
    db = pymysql.connect("localhost","root",sql_password,db="portfolio" )
    cur = db.cursor()
    cur.execute("SELECT * FROM HOLDINGS")

    ##SQL Queries
    name_query = "select company_name from stocks"
    ticker_query = "select ticker from stocks"
    h_ticker_query = "select ticker from holdings"
    pprice_query = "select purchase_price from holdings" 
    shares_query = "select shares from holdings"
    
    ##Converting SQL Queries to Lists
    cur.execute(name_query)
    name_list_raw = list(cur.fetchall())
    name_list = [i[0] for i in name_list_raw]
    
    cur.execute(ticker_query)
    ticker_list_raw = list(cur.fetchall())
    ticker_list = [i[0] for i in ticker_list_raw]
    
    cur.execute(h_ticker_query)
    h_ticker_list_raw = list(cur.fetchall())
    h_ticker_list = [i[0] for i in h_ticker_list_raw]
    
    cur.execute(pprice_query)
    pprice_list_raw = list(cur.fetchall())
    pprice_list = [float(i[0]) for i in pprice_list_raw]
    
    cur.execute(shares_query)
    shares_list_raw = list(cur.fetchall())
    shares_list = [float(i[0]) for i in shares_list_raw]
    
    ##Calling get_price() function and creating a dictionary with the current prices
    current_price_dict = {}
    try:
        for ticker in ticker_list:
            price = get_price(ticker)
            current_price_dict[ticker] = price
    except:
        return None
    
    ##Loop through current holdings to calculate gain on each and add them to a dictionary with distinct ticker keys
    ticker_gain_dict = {}
    for price_index, ticker in enumerate(h_ticker_list):
        indiv_gain = float((current_price_dict[ticker] - pprice_list[price_index])*shares_list[price_index])
        if ticker in list(ticker_gain_dict.keys()):
            ticker_gain_dict[ticker] = ticker_gain_dict[ticker] + indiv_gain
        else:
            ticker_gain_dict[str(ticker)] = indiv_gain

    ##Dictionary to convert Tickers to Company Names
    ticker_name_dict = dict(zip(ticker_list, name_list))
    
    ##Combine the Company Names with the Gains
    gain_dict = {}
    for ticker in ticker_gain_dict:
        gain_dict[ticker_name_dict[ticker]] = float("{0:.2f}".format(ticker_gain_dict[ticker]))

    return gain_dict

print(get_pnl())