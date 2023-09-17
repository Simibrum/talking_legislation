"""Tests for the XMLParser class."""
import os
import pytest
from bs4 import BeautifulSoup
from backend.common_logic.XMLparser import UKLegislationParser
from backend.tests.tests_logic import CURRENT_DIR


@pytest.fixture(autouse=True)
def mock_fetch_xml(mocker):
    def read_test_xml_file(path):
        full_path = os.path.join(CURRENT_DIR, path)
        with open(full_path, 'r') as file:
            return file.read()

    test_xml_content = read_test_xml_file('test_xml.xml')
    mocker.patch(
        'backend.common_logic.XMLparser.fetch_xml',
        return_value=BeautifulSoup(test_xml_content, 'lxml-xml'))


def test_read_and_parse_xml() -> None:
    """
    Test the _read_and_parse_xml method to ensure it successfully reads and parses the XML content.

    Returns:
        None
    """
    parser = UKLegislationParser('test_xml.xml')
    assert parser.soup is not None, "Failed to read and parse XML"


def test_parse_metadata() -> None:
    """
    Test the _parse_metadata method to ensure it populates the metadata dictionary.

    Returns:
        None
    """
    parser = UKLegislationParser('test_xml.xml')
    parser._parse_metadata()
    assert len(parser.metadata) > 0, "Failed to parse metadata"


def test_parse_contents() -> None:
    """
    Test the _parse_contents method to ensure it populates the contents dictionary.

    Returns:
        None
    """
    parser = UKLegislationParser('test_xml.xml')
    parser._parse_contents()
    assert len(parser.contents) > 0, "Failed to parse contents"
    assert 'parts' in parser.contents, "Failed to parse parts"
    assert 'blocks' in parser.contents['parts'][0], "Failed to parse blocks in parts"
    assert 'items' in parser.contents['parts'][0]['blocks'][0], "Failed to parse items in blocks"


def test_check_sections() -> None:
    """
    Test the _parse_contents method to ensure it correctly parses sections by their numbers.

    Returns:
        None
    """
    parser = UKLegislationParser('test_xml.xml')
    parser._parse_contents()

    # Define the expected section numbers
    expected_sections = [
        "1", "2", "3", "4", "4A", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14",
        "15", "15A", "16", "17", "18", "19", "20", "20A", "20B", "21", "22", "23", "24",
        "25", "26", "27", "28", "28A", "29", "30", "31", "32", "33", "34", "35", "36",
        "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "48A",
        "48B", "49", "50", "50A", "51", "52", "53", "54", "55", "56", "57", "57A", "58",
        "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "70A",
        "70B", "70C", "70D", "70E", "70F", "71", "72", "73", "74", "74A", "74B", "75",
        "76", "76A", "77", "78", "79", "80", "81", "82", "83", "83A", "84", "85", "86",
        "87", "88", "88A", "88B", "89", "89A", "89B", "90", "91", "92", "93", "94", "95",
        "96", "97", "98", "99", "99A", "99B", "100", "101", "102", "102A", "103", "104",
        "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116",
        "117", "117A", "117B", "118", "118A", "119", "120", "121", "122", "123", "124",
        "124A", "125", "125A", "126", "127", "128", "128A", "128B", "129", "130", "131",
        "131A", "132"
    ]

    # Traverse the parsed content to extract actual section numbers
    actual_sections = []
    for part in parser.contents['parts']:
        for block in part['blocks']:
            for item in block['items']:
                actual_sections.append(item['number'])

    assert (
        actual_sections == expected_sections,
        f"Expected sections do not match. Missing sections: {set(expected_sections) - set(actual_sections)}"
    )


@pytest.fixture
def mock_contents():
    return {
        'parts': [
            {
                'blocks': [
                    {
                        'items': [
                            {'DocumentURI': 'uri_1'},
                            {'DocumentURI': 'uri_2'}
                        ]
                    },
                    {
                        'items': [
                            {'DocumentURI': 'uri_3'}
                        ]
                    }
                ]
            },
            {
                'blocks': [
                    {
                        'items': [
                            {'DocumentURI': 'uri_4'}
                        ]
                    }
                ]
            }
        ]
    }


@pytest.fixture
def mock_fetch_simple_xml(mocker):
    """Mock fetch_xml method to return a dummy BeautifulSoup object."""
    mock_xml = "<xml>Dummy Data</xml>"
    return mocker.patch('backend.common_logic.XMLparser.fetch_xml', return_value=mock_xml)


def test_fetch_section_data(mock_fetch_simple_xml, mock_contents):
    parser = UKLegislationParser('dummy_uri')  # Initialize with a dummy URI

    # You might want to set parser.contents to a test dictionary mimicking your structure before calling the method.
    parser.contents = mock_contents

    parser._fetch_section_data()

    for part in parser.contents['parts']:
        for block in part['blocks']:
            for item in block['items']:
                assert 'xml_data' in item
                assert item['xml_data'] == "<xml>Dummy Data</xml>"  # This should match your mock XML data
