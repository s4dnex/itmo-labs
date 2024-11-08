# Author: Nikita "sadnex" Ryazanov

from typing import Any, Dict, List
from tokenizer import Tokenizer
from collections import OrderedDict

class Parser():
    # List of tokens of given string
    _tokens: List[Dict[str, Any]]
    # Dictionary of parsed tokens
    _dict: OrderedDict[str, Any]
    # Path to current scope
    _path: List[str]

    def __init__(self, string: str):
        tokenizer = Tokenizer(string)
        self._tokens = tokenizer.tokenize()
        self._dict = OrderedDict()
        self._path = []

    def __parse_token(self, token_ind: int = 0) -> OrderedDict[str, Any]:
        # Get current token
        token = self._tokens[token_ind]

        # Get previous and current scopes
        prev_scope = self._dict
        cur_scope = self._dict
        if self._path:
            for p in self._path[:-1]:
                prev_scope = prev_scope[p]
                cur_scope = cur_scope[p]
            cur_scope = cur_scope[self._path[-1]]

        if token['type'] == 'OPEN_TAG':
            # Add path to current scope
            self._path.append(token['name'])
            # Check if scope already exists
            if token['name'] not in cur_scope:
                # If not, check if it is array of values
                if isinstance(cur_scope, list):
                    # If it is array, add new element to the end
                    cur_scope.append(OrderedDict())
                    # Add path to the element
                    self._path.append(-1)
                else:
                    # If it is not array, create new scope
                    cur_scope[token['name']] = OrderedDict()
            else:
                # If scope exists, check if it is already array of scopes
                if isinstance(cur_scope[token['name']], list):
                    # If it is array, add new scope to the end
                    cur_scope[token['name']].append(OrderedDict())
                else:
                    # If it is not array, format to array of scopes
                    cur_scope[token['name']] = [cur_scope[token['name']], OrderedDict()]
                # Add path to the new scope (last element of the array of scopes)
                self._path.append(-1)
            
            # If there are attributes, add them to the scope
            if 'attributes' in token:
                cur_scope[token['name']].update({f'@{k}':v for k, v in token['attributes'].items()})

            # Move to the next token
            return self.__parse_token(token_ind + 1)

        elif token['type'] == 'CLOSE_TAG':
            # If current scope has no any value, set it to None
            if len(prev_scope[self._path[-1]]) == 0:
                prev_scope[self._path[-1]] = None

            # If current scope is element of an array, additionally delete path to its array 
            # Else, delete path to the current scope
            if self._path[-1] == -1:
                self._path.pop()
            self._path.pop()

            # Move to the next token
            return self.__parse_token(token_ind + 1)

        elif token['type'] == 'CONTENT':
            # If current scope is an array, add value to the end
            # Else, set the value
            if isinstance(prev_scope[self._path[-1]], list):
                prev_scope[self._path[-1]].append(token['value'])
            else:
                prev_scope[self._path[-1]] = token['value']
            # Move to the next token
            return self.__parse_token(token_ind + 1)

        elif token['type'] == 'COMMENT':
            # Skip comment and move to the next token
            return self.__parse_token(token_ind + 1)

        elif token['type'] == 'SELF_CLOSING_TAG':
            # Set scope of the current token to None as it is self-closing
            cur_scope[token['name']] = None
            # If there are attributes, add them to the scope
            if 'attributes' in token:
                cur_scope[token['name']] = OrderedDict({f'@{k}':v for k, v in token['attributes'].items()})
            # Move to the next token
            return self.__parse_token(token_ind + 1)

        elif token['type'] == 'EOF':
            # Return the dictionary as we parsed all tokens
            return self._dict

    def parse(self) -> OrderedDict[str, Any]:
        """
        Returns parsed string in the form of dictionary.
        """
        return self.__parse_token()