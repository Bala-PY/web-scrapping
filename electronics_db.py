import sqlite3
import api

# Create a new SQLite database (or connect to an existing one)
conn = sqlite3.connect('myntra_data.db')
c = conn.cursor()

# Creating a table to store the product details
c.execute('''
    CREATE TABLE IF NOT EXISTS electronics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        price TEXT,
        description TEXT,
        image_url TEXT,
        rating TEXT
    )
''')

# Inserting scraped data into the database
product_data = api.scrape_myntra_electronics()
for product in product_data:
    c.execute('''
        INSERT INTO electronics (product_name, price, description, image_url, rating)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        product['Product Name'],
        product['Price'],
        product['Description'],
        product['Image URL'],
        product['Rating'],  
    ))
    
print('Data import successful!')

# Commit and closing the connection
conn.commit()
conn.close()
