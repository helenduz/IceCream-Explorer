# [IceCream-Explorer](https://ice-cream-explorer.herokuapp.com/)

## Introduction
A website that allows users to search for ice cream products info from a large database. This is a team project for the _Software Design_ course at Carleton College, co-authored with Peter Tu @tutingjun and Yucheng Yang @YuchengY (we were all new to full-stack web development!). The data is retrieved from [**Kaggle**](https://www.kaggle.com/tysonpo/ice-cream-dataset). 

**Built with:**
- front-end: HTML, CSS, JavaScript 
- back-end: Flask
- database driver: Psycopg2
- databse: PostgreSQL
- application server: Gunicorn
- deployment: Heroku


## Requirements
This application is written in Python3 (last run with Python 3.9.4).
To run the webapp on Flask's development server, install the following packages:
- Psycopg2 (last run with psycopg 2.7.3)
- Flask (last run with Flask 0.12.2)
- PostgreSQL


## How to Run the Program on Flask's Development Server
1. Create a PostgreSQL database following [this guide](https://www.guru99.com/postgresql-create-database.html)
2. Create the tables with `psql -f createtable.sql`
3. Enter the psql CLI, then run the following:
```
\copy products FROM './Data/IceCreamData/products.csv' DELIMITER ',' CSV
\copy reviews FROM './Data/IceCreamData/reviews.csv' DELIMITER ',' CSV
```
4. Modify the `connection = psycopg2.connect(DATABASE_URL, sslmode='require')` line in datasource.py to 
```
connection = psycopg2.connect(database="", user="", password="", host="localhost")
```
where `database`, `user`, and `password` should be modified according to what you obtained in step 1
5. In the command line, type `python3 webapp.py 127.0.0.1 <port number>`, where `<port number>` can be an unused port number of your choice
6. In your web browser, go to `http://127.0.0.1:<port bumber>`, where `<port number>` is the port number you entered in the previous step


If you have access to the Perlman server (for Carleton College users only):
1. Connect to the Carleton VPN.
2. In the command line, type `ssh user@perlman.mathcs.carleton.edu`, where `user` should be replaced with your Carleton username.
3. After cloning this repository onto the Perlman server, navigate to the main folder. 
4. In the command line, type `python3 webapp.py perlman.mathcs.carleton.edu <port number>`, where `<port number>` can be 5107 or 5207.
5. In your web browser, go to `http://perlman.mathcs.carleton.edu:<port bumber>`, where `<port number>` is the port number you entered in the previous step.


## What It Does
Search for ice cream products by brand name, product name, ingredient, as well as many other filters (in the advance search section):

![Searching](demo/search.gif)

Rank products in search result:

![Ranking](demo/rank.gif)


Click on products on the list to view details:

![Details](demo/detail.gif)


Downloading the dataset and viewing metadata info: 

![Download](demo/download.gif "Downloading data and Viewing Metadata")


## Known Issues
If you use the browser back button when returning from product_list(product_list.html) to home page(index.html), and then hit the search button on the home page again, all products will be returned (the search filter will not work even though the conditions put in before will be there). In short: don't hit the browser back button when you are at the product_list(product_list.html) page. Click on the home page icon to go back to the home page when you want to initiate a new search.

## What's Next
- Create table and conduct queries using ORM (eg. SQLAlchemy) instead of plain SQL
