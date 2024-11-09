from typing import List
from xml_to_json import TAG_PATTERN, xml_list_to_string
import re

def __generate_tsv(match: tuple, path: str = ''):
    """
    Recursively replaces XML tag to JSON format (represented as a string).
    """
    global header, values
    # Check that match is not None
    if match:
        # Find all tags inside this tag
        next_matches = TAG_PATTERN.findall(match[1])
    
    # If there are nested tags
    if next_matches:
        for next_match in next_matches:
            __generate_tsv(next_match, path + match[0] + '.')
    
    else:
        header.append(path + match[0])
        values.append(match[1])


def convert(xml_list: List[str]) -> str:
    global header, values
    header = []
    values = []
    # Convert XML to string
    xml_str = xml_list_to_string(xml_list)

    main_tag = TAG_PATTERN.fullmatch(xml_str)
    main_tag = (main_tag.group(1), main_tag.group(2))
    __generate_tsv(main_tag)
    return '\t'.join(header) + '\n' + '\t'.join(values)


