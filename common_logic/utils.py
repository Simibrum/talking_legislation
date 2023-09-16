"""Common utility functions."""

from bs4 import BeautifulSoup, Tag
import requests
from typing import Union, Dict, List


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


def parse_element(element, depth: int = 0, parent_label: str = "") -> dict:
    """
    Recursively parses an XML element to extract legislative text and metadata.

    Parameters:
    - element: The XML element to parse (BeautifulSoup object)
    - depth: The current depth level in the XML tree (default is 0)
    - parent_label: The label for the parent element, used for nested elements (default is "")

    Returns:
    - dict: A dictionary containing the text and metadata for the legislative section
    """
    parsed_data = {
        'label': "",
        'full_label': "",
        'number': 0,
        'text': "",
        'subpoints': []
    }

    # Extract the label and number based on the depth
    if element.find("Pnumber"):
        label_text = element.find('Pnumber').text
        parsed_data['full_label'] = f"{parent_label}{label_text})"
        parsed_data['label'] = f"{label_text})"
        parsed_data['number'] = depth

    # Extract the text
    if element.find("Text"):
        parsed_data['text'] = ' '.join(element.find("Text").text.strip().split())

    # Recursively parse sub-elements
    for sub_element in element.find_all(["P2", "P3"], recursive=False):
        sub_parsed_data = parse_element(sub_element, depth=depth+1, parent_label=parsed_data['label'])
        parsed_data['subpoints'].append(sub_parsed_data)

    return parsed_data


def parse_recursive_old(element: Union[BeautifulSoup, None], depth: int = 1) -> Union[Dict, List]:
    if element is None:
        return {}

    parsed_data = {'subpoints': []}

    # Start looking for nested elements
    tag_name = f"P{depth}"
    para_tag_name = f"P{depth}para"
    nested_elements = element.find_all(tag_name)
    if nested_elements:
        for nested_element in nested_elements:
            number_element = nested_element.find(f"Pnumber")
            number = number_element.text.strip() if number_element else None

            # Look for <Pxpara> element
            para_element = nested_element.find(para_tag_name)
            text_element = nested_element.find("Text")
            text = ' '.join(element.find("Text").text.strip().split()) if text_element else None

            nested_data = parse_recursive(nested_element.find(f"P{depth}para"), depth=depth + 1)

            parsed_data['subpoints'].append({
                'label': number,
                'text': text,
                **nested_data
            })

    return parsed_data


def parse_recursive(element: Union[Tag, None], depth: int = 1) -> Union[Dict, List]:
    """
    Recursively parses an XML element to extract legislative text and metadata.

    Parameters:
        - element: The XML element to parse (BeautifulSoup object)
        - depth: The current depth level in the XML tree (default is 0)

    Returns:
        - Union[Dict, List]: A dictionary containing the text and metadata for the legislative section
        or a list of text/dictionary elements for nested sections.
        """
    if element is None:
        return {}

    parsed_data = {'text': []}

    # Start looking for nested elements
    para_tag_name = f"P{depth}para"

    useful_child_tags = ["Pnumber", para_tag_name]
    useful_children = element.find_all(useful_child_tags, recursive=False)
    if useful_children:
        for child in useful_children:
            # Check if the tag is a paragraph number
            if child.name == "Pnumber":
                parsed_data['label'] = child.text.strip()

            # Check if the tag is a paragraph content element
            elif child.name == para_tag_name:
                # Check for either text or deeper nested elements
                next_level = f"P{depth + 1}"
                para_children = child.find_all([next_level, "Text"], recursive=False)
                if para_children:
                    for para_child in para_children:
                        if para_child.name == next_level:
                            nested_data = parse_recursive(para_child, depth=depth + 1)
                            parsed_data['text'].append(nested_data)
                        elif para_child.name == "Text":
                            text = ' '.join(para_child.text.strip().split())
                            parsed_data['text'].append(text)

    return parsed_data


# Define the function to flatten the nested data structure and generate a text representation.
def flatten_text(data: dict, prefix: str = '', depth: int = 0) -> str:
    """
    Flattens a nested data structure to generate a text representation that includes the labels and text.

    Parameters:
        data (dict): The nested data structure containing 'text' and 'label' keys.
        prefix (str): The current prefix for the labels. Defaults to an empty string.
        depth (int): The current depth in the nested structure. Defaults to 0.

    Returns:
        str: The flattened text representation.
    """
    output = []
    if 'label' in data:
        # Don't add the first level - this is the section number and we will add separately with title
        if depth != 0:
            prefix = f"{prefix}{data['label']}) " if prefix else f"{data['label']}) "
    if 'text' in data:
        for item in data['text']:
            if isinstance(item, dict):
                output.append(flatten_text(item, prefix=prefix, depth=depth + 1))
            else:
                indent = '    ' * depth
                output.append(f"{indent}{prefix}{item}")
                prefix = ''
    return '\n'.join(output)
