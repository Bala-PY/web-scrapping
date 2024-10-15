import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

# Step 1: Setting up Selenium WebDriver
path = 'C:/Users/Bala Eesan/Downloads/chromedriver/chromedriver.exe'
service = Service(executable_path = path)
driver = webdriver.Chrome(service = service)

# Step 2: Opening the Myntra electronics section
URL = 'https://www.myntra.com/electronics'
driver.get(URL)

# Allowing time for the JavaScript to load the page
time.sleep(3)

# Step 3: Handling Pagination and Parsing the page with BeautifulSoup 
soup = BeautifulSoup(driver.page_source, 'html.parser')

next_button = driver.find_elements(by = 'xpath', value = '//a[@class="pagination-next"]')
while next_button:
    next_button.click()
    time.sleep(3)  # Wait for the new page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    next_button = driver.find_elements(by = 'xpath', value = '//a[@class="pagination-next"]')

# Step 4: Finding and extracting product details
products = soup.find_all('li', class_='product-base')

product_data = []

for product in products:
    # Get product name
    name_tag = product.find('h4', class_='product-product')
    product_name = name_tag.text if name_tag else 'N/A'

    # Get product price
    price_tag = product.find('span', class_='product-discountedPrice')
    product_price = price_tag.text if price_tag else 'N/A'

    # Get product image URL
    img_tag = product.find('img', class_='img-responsive')
    product_image = img_tag['src'] if img_tag else 'N/A'

    # Get product description
    desc_tag = product.find('h4', class_='product-product')
    product_description = desc_tag.text if desc_tag else 'N/A'

    # Get product rating
    rating_tag = product.find('div', class_='product-ratingsContainer')
    product_rating = rating_tag.text if rating_tag else 'N/A'


    # Storing the extracted data
    product_data.append({
        'Product Name': product_name,
        'Price': product_price,
        'Image URL': product_image,
        'Description': product_description,
        'Rating': product_rating,      
    })

     
# Step 5: Saving the data to CSV and JSON
df = pd.DataFrame(product_data)
df.to_csv('myntra_electronics.csv', index=False)
df.to_json('myntra_electronics.json')

# Closing the Selenium WebDriver
driver.quit()

print("Scraping completed and data saved as a CSV and JSON file")
