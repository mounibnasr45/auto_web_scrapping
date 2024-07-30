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

# Function to parse HTML content and extract text and links
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)  # Extract text with spacing and strip extra whitespace
    
    # Extract all links (URLs) from the page that start with "https://"
    links = [a.get('href') for a in soup.find_all('a', href=True) if a.get('href').startswith('https://')]
    
    return text, links

# Function to clean extracted text
def clean_text(text):
    clean_text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return clean_text.strip()

# Function to fetch and clean text from a URL
def fetch_and_clean_text_from_url(url):
    try:
        html_content = fetch_html_content(url)
        text, _ = parse_html(html_content)
        return clean_text(text)
    except Exception as e:
        return f"Failed to retrieve content from {url}: {e}"

# Main function to execute the web data extraction process
def main():
    try:
        url = get_url_input()
        
        # Fetch and clean text from the main URL
        html_content = fetch_html_content(url)
        raw_text, links = parse_html(html_content)
        clean_text_content = clean_text(raw_text)
        
        print("Extracted Text from the main page:")
        print(clean_text_content)
        
        print("\nExtracted Links:")
        for link in links:
            print(link)
        
        # Fetch and display text from each link after getting permission
        print("\nExtracted Texts from the linked pages:")
        for link in links:
            permission = input(f"Do you want to extract content from {link}? (yes/no): ").strip().lower()
            if permission == 'yes':
                print(f"\nContent from {link}:")
                print(fetch_and_clean_text_from_url(link))
            else:
                print(f"Skipping content extraction from {link}")
            
    except ValueError as ve:
        print(f"URL error: {ve}")
    except requests.RequestException as re:
        print(f"Request error: {re}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
