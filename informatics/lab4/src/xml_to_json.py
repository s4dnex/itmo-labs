# Author: Nikita "sadnex" Ryazanov

from typing import List
import xmltodict
import json
import re

JSON_INDENT = ' ' * 4
TAG_PATTERN = re.compile(r'<(?P<tag>.*?)>(.*?)</(?P=tag)>')

def xml_list_to_string(xml_list: List[str]) -> str:
    """
    Convert XML (represented as a list of strings) to string with removed leading and trailing whitespaces.
    """
    return ''.join([l.strip() if l.rstrip().endswith('>') else l.lstrip().replace('\n', '') 
                    for l in xml_list 
                    if (l.strip() and not(l.strip().endswith('?>')))
                    ])


# TODO: Handle XML comments and self-closing tags
def convert_raw(xml_list: List[str]) -> str:
    """
    Convert XML (represented as a list of strings) to JSON (represented as a string).
    This method doesn't use any libraries, regex and etc. 
    """
    # Convert XML to string
    xml_str = xml_list_to_string(xml_list)
    
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
    Convert XML (represented as a list of strings) to JSON (represented as a string).
    This method uses standard json library and xmltodict package by martinblech.
    """
    return json.dumps(
        xmltodict.parse(''.join(xml_list)), 
        ensure_ascii=False, 
        indent=JSON_INDENT
    )


def __replace_tag(match: tuple, unclosed_tags: int = 1) -> str:
    """
    Recursively replace XML tag to JSON format (represented as a string).
    """
    # Check that match is not None
    if match:
        # Find all tags inside this tag
        next_matches = TAG_PATTERN.findall(match[1])
    
    # If there are nested tags
    if next_matches:
        scope = []
        # Add curly bracket as we have nested tags
        scope.append(f'{JSON_INDENT * unclosed_tags}"{match[0]}":' + ' {')
        # Recursively add nested tags
        for next_match in next_matches:
            scope.append(f'{__replace_tag(next_match, unclosed_tags + 1)},')  
        # Remove comma from last tag
        scope[-1] = scope[-1][:-1]
        # Close current tag
        scope.append(f'{JSON_INDENT * unclosed_tags}' + '}')
        # Return current scope as a string
        return '\n'.join(scope)
    
    # If there are no nested tags return formatted tag as a key-value pair
    return f'{JSON_INDENT * unclosed_tags}"{match[0]}": "{match[1]}"'


# TODO: Handle XML comments and self-closing tags
def convert_regex(xml_list: List[str]) -> str:
    """
    Convert XML (represented in list of strings) to JSON (represented in string).
    This method uses regex.
    """
    # Convert XML to string
    xml_str = xml_list_to_string(xml_list)
    
    json_str = '{\n'
    
    # Find 1-level tags (main tags)
    main_tags = TAG_PATTERN.findall(xml_str)
    for main_tag in main_tags:
        # Add formatted tag
        json_str +=  __replace_tag(main_tag)

    # (Add closing bracket and) return JSON as a string 
    return json_str + '\n}'


