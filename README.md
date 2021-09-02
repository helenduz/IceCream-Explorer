# [IceCream-Explorer](https://ice-cream-explorer.herokuapp.com/)

## Introduction
A website that allows users to search for ice cream products info from a large database. This project is built upon a team project for the _Software Design_ course at Carleton College, co-authored with Peter Tu @tutingjun and Yucheng Yang @YuchengY (we were all new to full-stack web development!). The data is retrieved from [**Kaggle**](https://www.kaggle.com/tysonpo/ice-cream-dataset). 

**Built with:**
- front-end: HTML, CSS, JavaScript 
- back-end: Flask
- database driver: Psycopg2
- database: PostgreSQL
- application server: Gunicorn
- deployment: Heroku


## Requirements
This application is written in Python3 (last run with Python 3.9.4).
To run the webapp on Flask's development server, install the following packages:
- Psycopg2 (last run with psycopg 2.7.3)
- Flask (last run with Flask 0.12.2)
- PostgreSQL


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
