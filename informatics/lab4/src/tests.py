# Author: Nikita "sadnex" Ryazanov

import xml_to_json
import unittest
import os
import logging
import sys

def compare_files(file1: str, file2: str) -> bool:
    if len(file1) != len(file2):
        return False
    
    for i in range(len(file1)):
        if file1[i] != file2[i]:
            return False

    return True


class TestXMLToJSON(unittest.TestCase):
    filenames_convert = [f[:f.index('.')] for f in os.listdir('data/tests/convert') 
                         if os.path.isfile(os.path.join('data/tests/convert', f))
                         ]
    
    filenames_to_str = [f[:f.index('.')] for f in os.listdir('data/tests/xml_list_to_str')
                        if os.path.isfile(os.path.join('data/tests/xml_list_to_str', f))
                        ]

    

    def test_xml_list_to_string(self):
        log = logging.getLogger('TestXMLToJSON')
        log.debug('test_xml_list_to_string:\n')
        for filename in self.filenames_to_str:
            with open(rf'data\tests\xml_list_to_str\{filename}.xml', 'r', encoding='utf-8') as input, \
                open(rf'output\tests\xml_list_to_str\{filename}.xml', 'r', encoding='utf-8') as output:
                result = xml_to_json.xml_list_to_string(input.readlines())
                expected = output.readline()
                log.debug(f'{filename}:\n{result}')
                self.assertTrue(
                    compare_files(
                        result,
                        expected
                        )
                    )


    def test_convert_raw(self):
        log = logging.getLogger('TestXMLToJSON')
        log.debug('test_convert_raw:\n')
        for filename in self.filenames_convert:
            with open(rf'data\tests\convert\{filename}.xml', 'r', encoding='utf-8') as xml, \
                open(rf'output\tests\convert\{filename}.json', 'r', encoding='utf-8') as json:
                result = xml_to_json.convert_raw(xml.readlines())
                expected = ''.join(json.readlines())
                log.debug(f'{filename}:\n{result}')
                self.assertTrue(
                    compare_files(
                        result,
                        expected
                        )
                    )

    
    def test_convert_lib(self):
        log = logging.getLogger('TestXMLToJSON')
        log.debug('test_convert_lib:\n')
        for filename in self.filenames_convert:
            with open(rf'data\tests\convert\{filename}.xml', 'r', encoding='utf-8') as xml, \
                open(rf'output\tests\convert\{filename}.json', 'r', encoding='utf-8') as json: 
                result = xml_to_json.convert_lib(xml.readlines())
                expected = ''.join(json.readlines())
                log.debug(f'{filename}:\n{result}')
                self.assertTrue(
                    compare_files(
                        result,
                        expected
                        )
                    )
                

    def test_convert_regex(self):
        log = logging.getLogger('TestXMLToJSON')
        log.debug('test_convert_regex:\n')
        for filename in self.filenames_convert:
            with open(rf'data\tests\convert\{filename}.xml', 'r', encoding='utf-8') as xml, \
                open(rf'output\tests\convert\{filename}.json', 'r', encoding='utf-8') as json:
                result = xml_to_json.convert_regex(xml.readlines())
                expected = ''.join(json.readlines())
                log.debug(f'{filename}:\n{result}')
                self.assertTrue(
                    compare_files(
                        result,
                        expected
                        )
                    )


if __name__ == '__main__':
    if ('-log' in sys.argv):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('TestXMLToJSON').setLevel(logging.DEBUG)
    unittest.main(argv=['', '-v'])
