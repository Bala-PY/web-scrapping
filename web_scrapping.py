# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 07:22:17 2024

@author: Bala Eesan
"""

# Web Scrapping: List of Largest Companies in India_2023

from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_India'

try:
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')
except requests.exceptions.HTTPError as err:
    # Handle HTTP errors
    print(f'HTTP error occurred: {err}')

except requests.exceptions.ConnectionError as err:
    # Handle connection errors
    print(f'Connection error occurred: {err}')

except Exception as e:
    # Handle other parsing errors
    print(f'Error occurred while parsing HTML: {e}')

table = soup.find_all('table')[0]
table_headers = table.find_all('th')
table_headers_text = [header.text.strip() for header in table_headers]

df = pd.DataFrame(columns = table_headers_text)
column_data = table.find_all('tr')

for row in column_data[1:]:
  row_data = row.find_all('td')
  individual_row_data = [data.text.strip() for data in row_data]

  length = len(df)
  df.loc[length] = individual_row_data

df.to_csv('largest_companies.csv', index = False)