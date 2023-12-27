import requests
from bs4 import BeautifulSoup
from collections import Counter

# Website URL to scrape (replace with your target URL)
url = 'https://rvce.edu.in/mca'

try:
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        text_elements = soup.find_all(['strong'])
        # Extract the text from each element and concatenate them into a single string
        scraped_text = (element.get_text() for element in text_elements)
        p=list(scraped_text)
        for a in p:
            print(a)
        

    else:
        print('Failed to retrieve the web page.')

except Exception as e:
    print(f'An error occurred: {str(e)}')
