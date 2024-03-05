import requests
from bs4 import BeautifulSoup,SoupStrainer
import pandas as pd
import re
# Function to scrape data from the website
def scrape_laptops_data(url):
    # Send a request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 404:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html')
        print(soup)
        for link in soup.find_all('a', href=True):
            print(link['href'])
        paragraphs = soup.find_all('p')

        # Print each paragraph
        for idx, paragraph in enumerate(paragraphs, 1):
            print(f"Paragraph {idx}:")
            print(paragraph.get_text().strip())
            print("\n" + "=" * 50 + "\n")  # Separator for better readability
        all_text = soup.get_text(separator='\n', strip=True)

        # Print all text
        print(all_text)
        # Extract relevant information from the webpage
        laptop_data = []
        laptops = soup.find_all('div', class_='flex-item')
        for laptop in laptops:
            name = laptop.find('h3', class_='mb-0').text.strip()
            company = laptop.find('p', class_='company').text.strip()
            price = laptop.find('p', class_='price').text.strip()
            description = laptop.find('p', class_='description').text.strip()
            ram_spec = laptop.find('p', class_='ram').text.strip()

            # Append the data to the list
            laptop_data.append({
                'Laptop Name': name,
                'Company Name': company,
                'Laptop Price': price,
                'Description': description,
                'RAM Specifications': ram_spec
            })

        return laptop_data
    else:
        print(f"Failed to retrieve data. Status Code: {response.status_code}")
        return None
# URL of the website to scrape
url = "https://www.pcworld.com/article/436674/the-best-pc-laptops-of-the-year.html"
# Call the function to scrape data
laptop_data = scrape_laptops_data(url)

# Check if data is retrieved successfully
if laptop_data:
    # Create a DataFrame from the scraped data
    df = pd.DataFrame(laptop_data)
    # Display the DataFrame
    print(df)
    # Save the DataFrame to a CSV file
    df.to_csv('laptops_data.csv', index=False)
    print("Data saved to laptops_data.csv")
else:
    print("Failed to retrieve data.")