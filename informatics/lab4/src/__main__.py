# Author: Nikita "sadnex" Ryazanov
# Variant: 7


import xml_to_json

if __name__ == '__main__':
    xml_list = []

    with open(r'data\my_schedule.xml', 'r', encoding='utf-8') as f:
        xml_list = f.readlines()

    with open(r'output\my_schedule_raw.json', 'w', encoding='utf-8') as f:
        f.writelines(
            xml_to_json.convert_raw(xml_list)
        )

    with open(r'output\my_schedule_lib.json', 'w', encoding='utf-8') as f:
        f.writelines(
            xml_to_json.convert_lib(xml_list)
        )
    
    with open(r'output\my_schedule_regex.json', 'w', encoding='utf-8') as f:
        f.writelines(
            xml_to_json.convert_regex(xml_list)
        )
