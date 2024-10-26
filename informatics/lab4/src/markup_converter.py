# Author: Nikita "sadnex" Ryazanov
# Variant: 7

import xml_to_json

xml = []

with open(r'etc\my_schedule.xml', 'r', encoding='utf-8') as f:
    xml = f.readlines()

json = xml_to_json.convert_raw(xml)

with open(r'etc\my_schedule.json', 'w', encoding='utf-8') as f:
    f.writelines('\n'.join(json))