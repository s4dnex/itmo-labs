import time
from collections.abc import Callable
import xml_to_json

STRING_FORMAT = '{0:<20} {1:<20}'

def test_time(func: Callable) -> float:
    with open(r'data\my_schedule.xml', 'r', encoding='utf-8') as f:
        xml_list = f.readlines()
        start = time.perf_counter()
        for i in range(100):
            func(xml_list)
        end = time.perf_counter()
    return end - start


if __name__ == '__main__':
    print(STRING_FORMAT.format('Method', 'Time (in seconds)'))
    print(STRING_FORMAT.format('Raw', test_time(xml_to_json.convert_raw)))
    print(STRING_FORMAT.format('Library', test_time(xml_to_json.convert_lib)))
    print(STRING_FORMAT.format('RegEx', test_time(xml_to_json.convert_regex)))
    print(STRING_FORMAT.format('Formal Grammar', test_time(xml_to_json.convert_formal_grammar)))