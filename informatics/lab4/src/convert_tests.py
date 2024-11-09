# Author: Nikita "sadnex" Ryazanov

import xml_to_json
import unittest
import logging
from abc import ABC, abstractmethod
from collections.abc import Callable

STRING_FORMAT = '{0:<30} {1:<20} {2}'

def test_file(method: Callable, filename: str, log: logging.Logger = None) -> bool:
        """
        Compares the given XML file converted using given method with the pre-written JSON.

        Reads XML file with given name from data/tests directory, converts it using given method and compares with JSON from output/tests directory.
        If log is provided then method's result is logged with DEBUG level.
        """
        # Open XML and JSON files
        with open(rf'data\tests\{filename}.xml', 'r', encoding='utf-8') as xml, \
            open(rf'output\tests\{filename}.json', 'r', encoding='utf-8') as json:
            # Convert XML to JSON
            result = method(xml.readlines())
            # Log result if log is provided
            if log:
                log.debug(f'{filename}:\n{result}')
            # JSON to string
            expected = ''.join(json.readlines())
            # Compare converted XML and expected JSON
            return result == expected


# Abstract class for tests of different conversion methods
class TestConvert(ABC):
    @abstractmethod
    def test_basic(self):
        """
        Tests conversion of simple XML.
        """
        pass

    @abstractmethod
    def test_schedule(self):
        """
        Tests conversion of schedule.
        """
        pass
    
    @abstractmethod
    def test_comments(self):
        """
        Tests conversion of XML with comments.
        """
        pass

    @abstractmethod
    def test_array(self):
        """
        Tests conversion of XML with array.
        """
        pass
    
    @abstractmethod
    def test_empty_tags(self):
        """
        Tests conversion of XML with empty tags.
        """
        pass

    @abstractmethod
    def test_attributes(self):
        """
        Tests conversion of XML with attributes.
        """
        pass

    @abstractmethod
    def test_all_in_one(self):
        """
        Tests conversion of all-in-one XML.
        """
        pass
    

class MyTestResult(unittest.TextTestResult):
    # Create logger for test results
    log = logging.getLogger('TestConvert')
    log.setLevel(logging.INFO)
    log.addHandler(logging.FileHandler(r'output\logs\tests.log', 'w', 'utf-8'))

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.verbosity = verbosity


    def addSuccess(self, test):
        super().addSuccess(test)
        # Log test result
        self.log.info(STRING_FORMAT.format(test.__class__.__name__, test._testMethodName, 'PASS'))
          

    def addError(self, test, err):
        super().addError(test, err)
        # Log test result
        self.log.info(STRING_FORMAT.format(test.__class__.__name__, test._testMethodName, 'ERROR'))
            
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        # Log test result
        self.log.info(STRING_FORMAT.format(test.__class__.__name__, test._testMethodName, 'FAIL'))


# Tests of convert_raw method
class TestConvertRaw(TestConvert, unittest.TestCase):
    method = xml_to_json.convert_raw
    
    # Create logger for test results
    log = logging.getLogger('ConvertRaw')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.FileHandler(r'output\logs\convert_raw.log', 'w', 'utf-8'))
    
    def test_basic(self):
        self.assertTrue(test_file(self.method, 'test_basic', self.log))
    
    def test_schedule(self):
        self.assertTrue(test_file(self.method, 'test_schedule', self.log))
    
    def test_comments(self):
        self.assertTrue(test_file(self.method,'test_comments', self.log))
    
    def test_array(self):
        self.assertTrue(test_file(self.method, 'test_array', self.log))
    
    def test_empty_tags(self):
        self.assertTrue(test_file(self.method, 'test_empty_tags', self.log))

    def test_attributes(self):
        self.assertTrue(test_file(self.method, 'test_attributes', self.log))

    def test_all_in_one(self):
        self.assertTrue(test_file(self.method, 'test_all_in_one', self.log))


# Tests of convert_lib method
class TestConvertLib(TestConvert, unittest.TestCase):
    method = xml_to_json.convert_lib

    # Create logger for test results
    log = logging.getLogger('ConvertLib')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.FileHandler(r'output\logs\convert_lib.log', 'w', 'utf-8'))
    
    def test_basic(self):
        self.assertTrue(test_file(self.method, 'test_basic', self.log))
    
    def test_schedule(self):
        self.assertTrue(test_file(self.method, 'test_schedule', self.log))
    
    def test_comments(self):
        self.assertTrue(test_file(self.method,'test_comments', self.log))
    
    def test_array(self):
        self.assertTrue(test_file(self.method, 'test_array', self.log))
    
    def test_empty_tags(self):
        self.assertTrue(test_file(self.method, 'test_empty_tags', self.log))
    
    def test_attributes(self):
        self.assertTrue(test_file(self.method, 'test_attributes', self.log))
    
    def test_all_in_one(self):
        self.assertTrue(test_file(self.method, 'test_all_in_one', self.log))


# Tests of convert_regex method
class TestConvertRegex(TestConvert, unittest.TestCase):
    method = xml_to_json.convert_regex

    # Create logger for test results
    log = logging.getLogger('ConvertRegex')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.FileHandler(r'output\logs\convert_regex.log', 'w', 'utf-8'))
    
    def test_basic(self):
        self.assertTrue(test_file(self.method, 'test_basic', self.log))
    
    def test_schedule(self):
        self.assertTrue(test_file(self.method, 'test_schedule', self.log))
    
    def test_comments(self):
        self.assertTrue(test_file(self.method,'test_comments', self.log))
    
    def test_array(self):
        self.assertTrue(test_file(self.method, 'test_array', self.log))
    
    def test_empty_tags(self):
        self.assertTrue(test_file(self.method, 'test_empty_tags', self.log))

    def test_attributes(self):
        self.assertTrue(test_file(self.method, 'test_attributes', self.log))

    def test_all_in_one(self):
        self.assertTrue(test_file(self.method, 'test_all_in_one', self.log))


# Tests of convert_formal_grammar method
class TestConvertFormalGrammar(TestConvert, unittest.TestCase):
    method = xml_to_json.convert_formal_grammar

    # Create logger for test results
    log = logging.getLogger('ConvertFormalGrammar')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.FileHandler(r'output\logs\convert_formal_grammar.log', 'w', 'utf-8'))
    
    def test_basic(self):
        self.assertTrue(test_file(self.method, 'test_basic', self.log))
    
    def test_schedule(self):
        self.assertTrue(test_file(self.method, 'test_schedule', self.log))
    
    def test_comments(self):
        self.assertTrue(test_file(self.method,'test_comments', self.log))
    
    def test_array(self):
        self.assertTrue(test_file(self.method, 'test_array', self.log))
    
    def test_empty_tags(self):
        self.assertTrue(test_file(self.method, 'test_empty_tags', self.log))

    def test_attributes(self):
        self.assertTrue(test_file(self.method, 'test_attributes', self.log))

    def test_all_in_one(self):
        self.assertTrue(test_file(self.method, 'test_all_in_one', self.log))
     
        
if __name__ == '__main__':
    # Run all tests
    unittest.main(
        testRunner=unittest.TextTestRunner(
            resultclass=MyTestResult, verbosity=2
            )
        )
