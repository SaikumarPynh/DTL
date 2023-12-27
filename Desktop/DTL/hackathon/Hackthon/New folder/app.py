from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import sqlite3
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        # selectors = request.form.getlist('selectors')
        selectors_str = request.form['selectors']
        selectors = [s.strip() for s in selectors_str.split(',')]
        if url:
            scraped_data = scrape_data(url, selectors)
            return render_template('result.html', data=scraped_data)
    
    return render_template('index.html')

def scrape_data(url, selectors):
    # Scrape the website using requests and BeautifulSoup
    response = requests.get(url)
    if response.status_code != 200:
        return []

    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    scraped_data = {}

    # Connect to the SQLite database
    conn = sqlite3.connect('scraped_data.db')
    cursor = conn.cursor()

    for selector in selectors:
        # Find elements based on the user-defined selector
        elements = soup.select(selector)

        # Create a table for this selector
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {selector} (id INTEGER PRIMARY KEY, content TEXT)")

        # Insert the scraped data into the table
        for content in elements:
            cursor.execute(f"INSERT INTO {selector} (content) VALUES (?)", (content.text,))
        
        conn.commit()

        # Retrieve the data from the table
        cursor.execute(f"SELECT * FROM {selector}")
        table_data = cursor.fetchall()

        scraped_data[selector] = table_data

    conn.close()

    return scraped_data

if __name__ == '__main__':
    app.run(debug=True)
