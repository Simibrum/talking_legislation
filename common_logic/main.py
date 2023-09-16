# Initial dumping

from bs4 import BeautifulSoup

# Load the XML file
file_path = 'ukpga-1977-37-contents.xml'
with open(file_path, 'r', encoding='utf-8') as file:
    xml_content = file.read()

# Parse the XML content using Beautiful Soup
soup = BeautifulSoup(xml_content, 'lxml-xml')

# Preview of the root element and its direct children
root = soup.find_all(True, recursive=False)
root_info = {tag.name: len(tag.find_all(True, recursive=False)) for tag in root}
print(root_info)

# Explore the structure of the direct child elements under the root 'Legislation'
child_elements_info = {}
for child in soup.Legislation.find_all(True, recursive=False):
    child_elements_info[child.name] = len(child.find_all(True, recursive=False))

print(child_elements_info)


# Re-define the function to recursively explore the structure of an XML element
def explore_element_structure(element, depth=0, max_depth=2):
    if depth > max_depth:
        return "Max depth reached"

    child_structure = {}
    for child in element.find_all(True, recursive=False):
        child_structure[child.name] = explore_element_structure(child, depth + 1, max_depth)

    return child_structure


# Finally, retry exploring the structure of the 'Metadata' element
metadata_structure = explore_element_structure(soup.Legislation.Metadata)
print(metadata_structure)

# Explore the structure of the 'Contents' element
contents_structure = explore_element_structure(soup.Legislation.Contents)
print(contents_structure)

# Explore the structure of the 'Primary' element
primary_structure = explore_element_structure(soup.Legislation.Primary)
print(primary_structure)

# Explore the structure of the 'Commentaries' element
commentaries_structure = explore_element_structure(soup.Legislation.Commentaries)
print(commentaries_structure)

