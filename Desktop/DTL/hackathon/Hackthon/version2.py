import requests 
from bs4 import BeautifulSoup
import sqlite3

# Scrape the website as in your original code
url = 'https://rvce.edu.in'
response = requests.get(url)
if response.status_code == 200:
    html_content = response.content
else:
    print("Failed to fetch the website.")
    exit()

soup = BeautifulSoup(html_content, 'html.parser')
text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span'])
scraped_text = ' '.join(element.get_text() for element in text_elements)

# Connect to SQLite database (create one if it doesn't exist)
conn = sqlite3.connect('scraped_data.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Define a table structure (you can adjust this based on your data)
cursor.execute('''CREATE TABLE IF NOT EXISTS scraped_text (
                    id INTEGER PRIMARY KEY,
                    content TEXT
                 )''')

# Insert the scraped text into the database
cursor.execute("INSERT INTO scraped_text (content) VALUES (?)", (scraped_text,))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Scraped data has been stored in the database.")

import sqlite3
import tkinter as tk
from tkinter import Scrollbar, Text, Entry, Button

def retrieve_data():
    # Get the URL input from the Entry widget
    url = url_entry.get()

    # Connect to the SQLite database
    conn = sqlite3.connect('scraped_data.db')
    cursor = conn.cursor()

    # Execute an SQL query to select data from the table
    cursor.execute("SELECT * FROM scraped_text")
    rows = cursor.fetchall()

    # Clear the existing text in the Text widget
    text_widget.delete(1.0, tk.END)

    # Display the content in the Text widget
    for row in rows:
        text_widget.insert(tk.END, row[1] + '\n')  # Assuming the content is in the second column (index 1)

    # Close the connection
    conn.close()

# Create a Tkinter window
window = tk.Tk()
window.title("Scraped Data Viewer")

# Create an Entry widget for entering the website URL
url_label = tk.Label(window, text="Website URL:")
url_label.pack()
url_entry = Entry(window, width=40)
url_entry.pack()

# Create a Text widget to display the data
text_widget = Text(window, wrap=tk.WORD, width=50, height=20)
text_widget.pack()

# Create a Scrollbar for the Text widget
scrollbar = Scrollbar(window, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget.config(yscrollcommand=scrollbar.set)

# Create a button to retrieve and display data
retrieve_button = Button(window, text="Retrieve Data", command=retrieve_data)
retrieve_button.pack()

# Start the Tkinter event loop
window.mainloop()

