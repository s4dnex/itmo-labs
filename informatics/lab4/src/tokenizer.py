# Author: Nikita "sadnex" Ryazanov

import re
from typing import Any, Dict, List

# Formal Grammar
CHAR = r'.'
WHITESPACE = r'\s'
NAME = r'[a-zA-Z][a-zA-Z0-9_]*'
COMMENT = rf'<!--({CHAR}*?)-->'
EQ = rf'{WHITESPACE}?={WHITESPACE}?'
ATTRIBUTE_VALUE = rf'"[^<\&"]*?"'
ATTRIBUTE = rf'({NAME}){EQ}({ATTRIBUTE_VALUE})'
OPEN_TAG = rf'<({NAME})(({WHITESPACE}{ATTRIBUTE})*?){WHITESPACE}?>'
CLOSE_TAG = rf'</({NAME}){WHITESPACE}?>'
CONTENT = rf'([^<\&]*)?'
SELF_CLOSING_TAG = rf'<({NAME})(({WHITESPACE}{ATTRIBUTE})*?){WHITESPACE}?/>'

TOKENS = [
    # (Regex, Token type)
    (re.compile(COMMENT), 'COMMENT'),
    (re.compile(OPEN_TAG), 'OPEN_TAG'),
    (re.compile(CLOSE_TAG), 'CLOSE_TAG'),
    (re.compile(SELF_CLOSING_TAG), 'SELF_CLOSING_TAG'),
    (re.compile(CONTENT), 'CONTENT')
]


class Tokenizer:
    # String to tokenize
    _string: str
    # Index of current position
    _ind: int
    
    def __init__(self, string: str):
        self._string = string
        self._ind = 0
    
    def has_tokens_left(self):
        """
        Checks if there are tokens left in the string.
        """
        return self._ind < len(self._string)
    
    def format_token(self, token_type: str, match: re.Match[str] | None) -> dict[str, Any]:
        """
        Formats token into dictionary.
        """
        # Create dictionary with token type
        token = {
            'type': token_type
        }
        if token_type == 'OPEN_TAG' or token_type == 'SELF_CLOSING_TAG':
            # Add name of tag to dictionary
            token['name'] = match.group(1)
            # Add attributes to dictionary
            if (token_type == 'OPEN_TAG' or token_type == 'SELF_CLOSING_TAG') and match.group(2):
                token['attributes'] = {att[0]:(att[1][1:-1] if att[1][0] == '"' and att[1][-1] == '"' else att[1]) 
                                       for att in re.findall(ATTRIBUTE, match.group(2))}
        elif token_type == 'CLOSE_TAG':
            # Add name of tag to dictionary
            token['name'] = match.group(1)
        elif token_type == 'CONTENT':
            # Add value to dictionary
            token['value'] = match.group(0)
        elif token_type == 'COMMENT':
            # Add value to dictionary
            token['value'] = match.group(1)
        return token


    def get_next_token(self) -> dict[str, Any] | None:
        """
        Finds next token in the string.
        Returns None if token is not found.
        """
        # Get string from current position
        string = self._string[self._ind:]

        # Try to match string with one of the tokens
        for regex, token_type in TOKENS:
            if match := regex.match(string):
                # Move current position
                self._ind += len(match.group(0))
                # Return formatted token
                return self.format_token(token_type, match)
        # If token is not found
        return None
        
    def tokenize(self) -> List[Dict[str, Any]]:
        # List of tokens in string
        tokens = []
        # While there are tokens left
        while self.has_tokens_left():
            if token := self.get_next_token():
                # Add token to list
                tokens.append(token)
            else:
                # If token is not found
                raise Exception(f'Unrecognized token from index {self._ind}: {self._string[self._ind:self._ind+10]}...')
        # Add end of file token
        tokens.append({'type': 'EOF'})
        return tokens