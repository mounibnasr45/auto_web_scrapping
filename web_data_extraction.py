import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Function to accept and validate URL input
def get_url_input():
    url = input("Enter the URL: ")  # Prompting the user to enter the URL
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("Invalid URL format. URL must start with 'http://' or 'https://'")
    return url

# Function to fetch HTML content from a URL
def fetch_html_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text

# Function to parse HTML content and extract text
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)  # Extract text with spacing and strip extra whitespace
    return text

# Function to handle dynamic content using Selenium
def fetch_dynamic_content(url):
    options = Options()
    options.headless = True
    service = Service(executable_path=r'C:\Users\mouni\Downloads\chromedriver-win64\chromedriver.exe')  # Correct path to your chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    html_content = driver.page_source
    driver.quit()
    return html_content

# Function to clean extracted text
def clean_text(text):
    clean_text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return clean_text.strip()

# Main function to execute the web data extraction process
def main():
    try:
        url = get_url_input()
        
        # Choose the method to fetch HTML content based on the URL
        html_content = fetch_html_content(url)
        
        raw_text = parse_html(html_content)
        clean_text_content = clean_text(raw_text)
        print(clean_text_content)
    except ValueError as ve:
        print(f"URL error: {ve}")
    except requests.RequestException as re:
        print(f"Request error: {re}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
