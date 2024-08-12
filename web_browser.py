import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching page: {e}")
        return None

def render_page(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Rewrite links to open within the app
    for link in soup.find_all("a"):
        href = link.get("href")
        if href:
            link['href'] = f'?url={urljoin(base_url, href)}'

    return str(soup)

# Set up Streamlit app
st.title("Web Browser")

# URL input
url = st.text_input("Enter a URL", "https://www.hackclub.com")

# Fetch and display the page when the button is pressed
if st.button("Go"):
    if not urlparse(url).scheme:
        url = "http://" + url

    html_content = fetch_page(url)
    if html_content:
        st.components.v1.html(render_page(html_content, url), height=600, scrolling=True)
