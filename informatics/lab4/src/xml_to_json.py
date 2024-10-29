# Author: Nikita "sadnex" Ryazanov

from typing import List
import xmltodict
import json
import re


JSON_INDENT = ' ' * 4


def xml_list_to_string(xml_list: List[str]) -> str:
    """
    Convert XML (represented in list of strings) to string.
    """
    return ''.join([l.strip() for l in xml_list if l.strip()])


def convert_raw(xml_list: List[str]) -> str:
    """
    Convert XML (represented in list of strings) to JSON (represented in string).
    This method doesn't use any libraries, regex and etc. 
    """

    xml_str = xml_list_to_string(xml_list)
    xml_str = xml_str[xml_str.index('?>') + 2:]
    
    # List of JSON strings
    json_list = ['{']
    # Index of current bracket
    br = -1
    # Counter of unclosed tags
    unclosed_tags = 0

    # List of tag brackets in order
    brs = []
    for i in range(len(xml_str)):
        if xml_str[i:i+2] == '</':
            brs.append('</')
        elif xml_str[i] == '<':
            brs.append('<')
    
    i = 0
    while i < len(xml_str):
        if xml_str[i:i + 2] == '</':
            br += 1
            unclosed_tags -= 1

            # If last bracket then exit loop
            if (br + 1) >= len(brs):
                break

            # If next tag is closing tag too then this tag is nested, so close parent tag with curly bracket 
            if brs[br + 1] == '</':
                json_list.append(JSON_INDENT * unclosed_tags + '}' + \
                # If there is another tag after this then add comma                            
                            (',' if (br + 1 < len(brs) and brs[br + 1] == '<') else ''))
            # If next tag is opening tag then add comma
            else:
                json_list[-1] += ','

            # Move to end of this tag
            i = xml_str.index('>', i + 1)
        
        elif xml_str[i] == '<':
            br += 1
            unclosed_tags += 1
            # Add formatted tag to key
            json_list.append(JSON_INDENT * unclosed_tags + '"' + xml_str[i + 1: xml_str.index('>', i + 1)] + '": ')
            # Move to end of this tag
            i = xml_str.index('>', i + 1)
        
        elif xml_str[i] == '>':
            # If next tag is opening tag too then add curly bracket (because next tag is nested in this)
            if brs[br] == '<' and brs[br + 1] == '<':
                json_list[-1] += '{'
            # Increment index
            i += 1
        
        else:
            # Add value of current tag to last key
            json_list[-1] += '"' + xml_str[i:xml_str.index('</', i + 1)] + '"'
            # Move to closing tag
            i = xml_str.index('</', i + 1)
    
    # Add closing bracket of JSON file
    json_list.append('}')
    return '\n'.join(json_list)


def convert_lib(xml_list: List[str]) -> str:
    """
    Convert XML (represented in list of strings) to JSON (represented in string).
    This method uses standard json library and xmltodict package by martinblech.
    """
    return json.dumps(
        xmltodict.parse(''.join(xml_list)), 
        ensure_ascii=False, 
        indent=JSON_INDENT
    )


def convert_regex(xml_list: List[str]) -> str:
    """
    Convert XML (represented in list of strings) to JSON (represented in string).
    This method uses regex.
    """
    xml_str = xml_list_to_string(xml_list)
    xml_str = xml_str[xml_str.index('?>') + 2:]

    json_list = ['{']

    open_tag_pattern = re.compile(r'<(.*?)>')
    close_tag_pattern = re.compile(r'</(.*?)>')
    value_pattern = re.compile(r'>(.*?)<')

    i = 0
    tags = []
    while i < len(xml_str):
        if match := close_tag_pattern.match(xml_str, i):
            tags.append(("close_tag", match.group(1)))
            i += len(match.group(0))
        elif match := open_tag_pattern.match(xml_str, i):
            tags.append(("open_tag", match.group(1)))
            i += len(match.group(0))
        elif match := value_pattern.match(xml_str, i - 1):
            tags.append(("value", match.group(1)))
            i += len(match.group(1)) 
        else:
            raise ValueError(f"Invalid XML")
        
    unclosed_tags = 0
    for i in range(len(tags) - 1):
        type, value = tags[i]
        
        if type == "open_tag":
            unclosed_tags += 1
            json_list.append(
                JSON_INDENT * unclosed_tags + \
                '"' + value + '": ' + \
                ('{' if  ((i+1) < len(tags)) and (tags[i + 1][0] == "open_tag") else '')
            )

        elif type == "close_tag":
            unclosed_tags -= 1
            if tags[i + 1][0] == "close_tag":
                json_list.append(
                    JSON_INDENT * unclosed_tags + \
                    '}' + \
                    (',' if ((i+1) < len(tags)) and (tags[i + 1][0] == "open_tag") else '')
                )
            elif tags[i + 1][0] == "open_tag":
                json_list[-1] += ','

        elif type == "value":
            json_list[-1] += '"' + value + '"'

    json_list.append('}')

    return '\n'.join(json_list)