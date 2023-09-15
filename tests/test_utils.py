"""Test for utility functions in utils.py."""

import pytest
from bs4 import BeautifulSoup
from utils import fetch_xml, parse_recursive



def test_fetch_xml_success(mocker):
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, content='<xml><tag>content</tag></xml>'))
    result = fetch_xml('http://test.com')
    expected_result = BeautifulSoup('<xml><tag>content</tag></xml>', 'xml')
    assert str(result) == str(expected_result)


def test_fetch_xml_failure(mocker):
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=404))
    result = fetch_xml('http://test.com')
    assert result is None


def test_fetch_xml_exception(mocker):
    mocker.patch('requests.get', side_effect=Exception("An error occurred."))
    result = fetch_xml('http://test.com')
    assert result is None


def test_parse_recursive():
    with open('test_section.xml', 'r') as f:
        soup = BeautifulSoup(f, 'lxml-xml')

    # primary_element = soup.find('Primary')
    primary_element = soup.find('P1')
    parsed_data = parse_recursive(primary_element)

    assert parsed_data['label'] == "1"
    assert len(parsed_data['text']) == 5

    # Assertions for the first subpoint
    assert isinstance(parsed_data['text'][0]['text'][0], str)
    assert isinstance(parsed_data['text'][0]['text'][5], str)
    assert isinstance(parsed_data['text'][0]['text'][1], dict)
    assert isinstance(parsed_data['text'][0]['text'][2], dict)
    assert isinstance(parsed_data['text'][0]['text'][3], dict)
    assert isinstance(parsed_data['text'][0]['text'][4], dict)
    assert parsed_data['text'][0]['text'][0] == ('A patent may be granted only for an invention in respect of which '
                                                 'the following conditions are satisfied, that is to say—')
    assert parsed_data['text'][0]['text'][1]['label'] == "a"
    assert parsed_data['text'][0]['text'][1]['text'] == ["the invention is new;"]
    assert parsed_data['text'][0]['text'][5] == ('and references in this Act to a patentable invention '
                                                 'shall be construed accordingly.')

    for i, item in enumerate(parsed_data['text'], start=1):
        assert item['label'] == str(i)

    with open('test_section_2.xml', 'r') as f:
        soup = BeautifulSoup(f, 'lxml-xml')

    primary_element = soup.find('P1')
    parsed_data = parse_recursive(primary_element)
    assert parsed_data['label'] == "129"
    assert len(parsed_data['text']) == 1
    assert parsed_data['text'][0] == ('—This Act does not affect Her Majesty in her private capacity but, '
                                      'subject to that, it binds the Crown.')