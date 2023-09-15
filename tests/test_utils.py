"""Test for utility functions in utils.py."""

import pytest
from utils import fetch_xml
from bs4 import BeautifulSoup


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
