import os
import requests
from bs4 import BeautifulSoup


def ensure_directory(path):
    """Ensure directory exists"""
    if not os.path.exists(path):
        os.makedirs(path)


def fetch_url_content(url):
    """Fetch URL content"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        raise Exception(f"Failed to fetch URL content: {str(e)}")


def extract_title(html):
    """Extract title from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    return title.text if title else 'Untitled'


def sanitize_filename(filename):
    """Sanitize filename"""
    import re
    return re.sub(r'[^a-zA-Z0-9_-]', '_', filename)


def read_file(file_path):
    """Read file content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_path, content):
    """Write file content"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
