"""Common utility functions."""

from bs4 import BeautifulSoup
import requests
from typing import Union


def fetch_xml(base_url: str) -> Union[BeautifulSoup, None]:
    """
    Fetch XML data from the given URL endpoint and parse it using BeautifulSoup.

    Parameters:
    - base_url (str): The base URL where the XML resides.

    Returns:
    - BeautifulSoup object containing the parsed XML if successful, None otherwise.
    """
    try:
        # Append 'data.xml' to the base URL
        full_url = f"{base_url}/data.xml"

        # Fetch the XML data
        response = requests.get(full_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the XML using BeautifulSoup
            soup = BeautifulSoup(response.content, 'xml')
            return soup
        else:
            print(f"Failed to fetch XML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
