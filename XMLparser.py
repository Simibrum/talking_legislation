# Code for the legislation XML parser
from typing import Dict, Any, Optional, List
from bs4 import BeautifulSoup


class UKLegislationParser:
    def __init__(self, path):
        # Initialize internal data structures
        self.metadata = {}
        self.contents = {}
        self.primary = {}
        self.commentaries = {}

        # Read and parse XML
        self._read_and_parse_xml(path)

    def _read_and_parse_xml(self, path: str) -> None:
        """
        Read the XML content from the given path and initialize the BeautifulSoup object.

        Parameters:
            path (str): The path to the XML file.

        Returns:
            None
        """
        try:
            with open(path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
            self.soup = BeautifulSoup(xml_content, 'lxml-xml')
        except Exception as e:
            print(f"An error occurred: {e}")
            self.soup = None

    def _parse_metadata(self) -> None:
        """
        Parse and populate the metadata section from the XML content.

        Returns:
            None
        """
        metadata_element = self.soup.find('Metadata')
        if metadata_element is None:
            print("Metadata section not found in XML.")
            return

        for child in metadata_element.find_all(True, recursive=False):
            self.metadata[child.name] = child.text.strip()

    def _parse_contents(self) -> None:
        """
        Parse and populate the contents section from the XML content.

        Returns:
            None
        """
        contents_element = self.soup.find('Contents')
        if contents_element is None:
            print("Contents section not found in XML.")
            return

        self.contents['title'] = contents_element.ContentsTitle.text if contents_element.ContentsTitle else None

        self.contents['parts'] = []
        for part in contents_element.find_all('ContentsPart', recursive=False):
            part_dict: Dict[str, Any] = {}
            part_dict['number'] = part.ContentsNumber.text if part.ContentsNumber else None
            part_dict['title'] = part.ContentsTitle.text if part.ContentsTitle else None

            # Capture individual blocks within each part
            part_dict['blocks'] = self._parse_blocks(part)

            self.contents['parts'].append(part_dict)

    def _parse_blocks(self, part_element) -> List[Dict[str, Any]]:
        """
        Parse and return individual blocks within a given part.

        Parameters:
            part_element (BeautifulSoup element): The BeautifulSoup element representing a part.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing individual blocks.
        """
        blocks = []
        for block in part_element.find_all('ContentsPblock', recursive=False):
            block_dict: Dict[str, Any] = {}
            block_dict['title'] = block.ContentsTitle.text if block.ContentsTitle else None

            # Capture individual items within each block
            block_dict['items'] = self._parse_items(block)

            blocks.append(block_dict)
        return blocks

    def _parse_items(self, block_element) -> List[Dict[str, Any]]:
        """
        Parse and return individual items within a given block.

        Parameters:
            block_element (BeautifulSoup element): The BeautifulSoup element representing a block.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing individual items.
        """
        items = []
        for item in block_element.find_all('ContentsItem', recursive=False):
            item_dict: Dict[str, Any] = {}
            item_dict['number'] = item.ContentsNumber.text if item.ContentsNumber else None
            item_dict['title'] = item.ContentsTitle.text if item.ContentsTitle else None
            item_dict['IdURI'] = item.get('IdURI', None)
            item_dict['DocumentURI'] = item.get('DocumentURI', None)
            items.append(item_dict)
        return items

    def _parse_primary(self):
        # Populate self.primary
        pass

    def _parse_commentaries(self):
        # Populate self.commentaries
        pass

    def get_metadata(self):
        return self.metadata

    def get_contents(self):
        return self.contents

    # ... more public methods
