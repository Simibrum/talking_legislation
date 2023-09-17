"""Test for utility functions in utils.py."""
import os
from bs4 import BeautifulSoup
from backend.common_logic.utils import fetch_xml, parse_recursive, flatten_text
from backend.tests.tests_logic import CURRENT_DIR

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
    full_path = os.path.join(CURRENT_DIR, 'test_section.xml')
    with open(full_path, 'r') as f:
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

    full_path2 = os.path.join(CURRENT_DIR, 'test_section_2.xml')
    with open(full_path2, 'r') as f:
        soup = BeautifulSoup(f, 'lxml-xml')

    primary_element = soup.find('P1')
    parsed_data = parse_recursive(primary_element)
    assert parsed_data['label'] == "129"
    assert len(parsed_data['text']) == 1
    assert parsed_data['text'][0] == ('—This Act does not affect Her Majesty in her private capacity but, '
                                      'subject to that, it binds the Crown.')


nested_data = {
    'text': [
        {
            'text': [
                'A patent may be granted only for an invention in respect of which the following conditions are satisfied, that is to say—',
                {'text': ['the invention is new;'], 'label': 'a'},
                {'text': ['it involves an inventive step;'], 'label': 'b'},
                {'text': ['it is capable of industrial application;'], 'label': 'c'},
                {'text': ['the grant of a patent for it is not excluded by subsections (2) and (3) or section 4A below;'], 'label': 'd'},
                'and references in this Act to a patentable invention shall be construed accordingly.'
            ],
            'label': '1'
        },
        {
            'text': [
                'It is hereby declared that the following (among other things) are not inventions for the purposes of this Act, that is to say, anything which consists of—',
                {'text': ['a discovery, scientific theory or mathematical method;'], 'label': 'a'},
                {'text': ['a literary, dramatic, musical or artistic work or any other aesthetic creation whatsoever;'], 'label': 'b'},
                {'text': ['a scheme, rule or method for performing a mental act, playing a game or doing business, or a program for a computer;'], 'label': 'c'},
                {'text': ['the presentation of information;'], 'label': 'd'},
                'but the foregoing provision shall prevent anything from being treated as an invention for the purposes of this Act only to the extent that a patent or application for a patent relates to that thing as such.'
            ],
            'label': '2'
        },
        {'text': ['A patent shall not be granted for an invention the commercial exploitation of which would be contrary to public policy or morality.'], 'label': '3'},
        {'text': ['For the purposes of subsection (3) above exploitation shall not be regarded as contrary to public policy or morality only because it is prohibited by any law in force in the United Kingdom or any part of it.'], 'label': '4'},
        {'text': ['The Secretary of State may by order vary the provisions of subsection (2) above for the purpose of maintaining them in conformity with developments in science and technology; and no such order shall be made unless a draft of the order has been laid before, and approved by resolution of, each House of Parliament.'], 'label': '5'}
    ],
    'label': '1'
}


def test_flatten_text():
    """Test flattening the text."""
    text = flatten_text(nested_data)
    expected_text = """    1) A patent may be granted only for an invention in respect of which the following conditions are satisfied, that is to say—
        a) the invention is new;
        b) it involves an inventive step;
        c) it is capable of industrial application;
        d) the grant of a patent for it is not excluded by subsections (2) and (3) or section 4A below;
    and references in this Act to a patentable invention shall be construed accordingly.
    2) It is hereby declared that the following (among other things) are not inventions for the purposes of this Act, that is to say, anything which consists of—
        a) a discovery, scientific theory or mathematical method;
        b) a literary, dramatic, musical or artistic work or any other aesthetic creation whatsoever;
        c) a scheme, rule or method for performing a mental act, playing a game or doing business, or a program for a computer;
        d) the presentation of information;
    but the foregoing provision shall prevent anything from being treated as an invention for the purposes of this Act only to the extent that a patent or application for a patent relates to that thing as such.
    3) A patent shall not be granted for an invention the commercial exploitation of which would be contrary to public policy or morality.
    4) For the purposes of subsection (3) above exploitation shall not be regarded as contrary to public policy or morality only because it is prohibited by any law in force in the United Kingdom or any part of it.
    5) The Secretary of State may by order vary the provisions of subsection (2) above for the purpose of maintaining them in conformity with developments in science and technology; and no such order shall be made unless a draft of the order has been laid before, and approved by resolution of, each House of Parliament."""
    assert text == expected_text