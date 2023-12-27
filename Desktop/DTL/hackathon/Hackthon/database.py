import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('scraped_data.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute an SQL query to select data from the table
cursor.execute("SELECT * FROM scraped_text")

# Fetch all rows of data
rows = cursor.fetchall()

# Loop through the rows and print the content
for row in rows:
    print(row[1])  # Assuming the content is in the second column (index 1)

# Close the connection
conn.close()
