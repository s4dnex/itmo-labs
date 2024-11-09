from typing import List
from xml_to_json import TAG_PATTERN, xml_list_to_string


def __generate_tsv(match: tuple, path: str = ''):
    """
    Recursively replaces XML tag to TSV format.
    """
    global header, values
    # Check that match is not None
    if match:
        # Find all tags inside this tag
        next_matches = TAG_PATTERN.findall(match[1])
    
    # If there are nested tags
    if next_matches:
        # Recursively add nested tags
        for next_match in next_matches:
            __generate_tsv(next_match, path + match[0] + '.')
    # If there are no nested tags return formatted tag as a TSV value
    else:
        header.append(path + match[0])
        values.append(match[1])


def convert(xml_list: List[str]) -> str:
    """
    Converts XML (represented in list of strings) to TSV (represented in string).
    """
    global header, values
    header = []
    values = []
    # Convert XML to string
    xml_str = xml_list_to_string(xml_list)
    # Find root tag
    main_tag = TAG_PATTERN.fullmatch(xml_str)
    main_tag = (main_tag.group(1), main_tag.group(2))
    # Format root tag
    __generate_tsv(main_tag)
    return '\t'.join(header) + '\n' + '\t'.join(values)


