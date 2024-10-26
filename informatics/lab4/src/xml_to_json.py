from typing import List
from collections import deque

INDENT = ' ' * 4

def convert_raw(xml: List[str]) -> List[str]:
    xml = ''.join([l.strip() for l in xml if l.strip()])
    xml = xml[xml.index('?>') + 2:]
    
    json = ['{']
    br = -1
    unclosed_tags = 0

    brs = deque()

    for i in range(len(xml)):
        if xml[i:i+2] == '</':
            brs.append('</')
        elif xml[i] == '<':
            brs.append('<')
    
    i = 0
    while i < len(xml):
        if xml[i:i + 2] == '</':
            br += 1
            unclosed_tags -= 1

            if (br + 1) >= len(brs):
                break

            if brs[br + 1] == '</':
                json.append(INDENT * unclosed_tags + '}' + (',' if (br + 1 < len(brs) and brs[br + 1] == '<') else ''))
            else:
                json[-1] += ','

            i = xml.index('>', i + 1)
        
        elif xml[i] == '<':
            br += 1
            unclosed_tags += 1
            json.append(INDENT * unclosed_tags + '"' + xml[i + 1: xml.index('>', i + 1)] + '": ')
            i = xml.index('>', i + 1)
        
        elif xml[i] == '>':
            if brs[br] == '<' and brs[br + 1] == '<':
                json[-1] += '{'
            i += 1
        
        else:
            json[-1] += '"' + xml[i:xml.index('</', i + 1)] + '"'
            i = xml.index('</', i + 1)
    
    json.append('}')
    return json


def test(xml: List[str]) -> List[str]:
    json = ['{\n']
    stack = deque()
    index = -1
    open_tags = 0
    closed_tags = 0

    for l in xml[1:]:
        l = l.strip()
        for i in range(len(l)):
            if l[i:i+2] == '</':
                stack.append('</')
        #         stack.pop()
        #         break
            elif l[i] == '<':
                stack.append('<')
        #         cur_str += INDENT * len(stack) + '"'
        #     elif l[i] == '>':
        #         cur_str += '": {'
        #     else:
        #         cur_str += l[i]
        
        # if cur_str:
        #     json += cur_str + "\n" + INDENT * (len(stack) - 1) + "},\n"
    
    for l in xml[1:]:
        cur_str = ''
        l = l.strip()
        for i in range(len(l)):
            if l[i:i+2] == '</':
                closed_tags += 1
                if stack[index + 1] == '</':
                    cur_str += INDENT * (open_tags - closed_tags - 1) + '},\n'
                index += 1
                break
            elif l[i] == '<':
                open_tags += 1
                cur_str += INDENT * (open_tags - closed_tags) + '"'
                index += 1
            elif l[i] == '>':
                cur_str += '": '
                if stack[index + 1] == '<':
                    cur_str += '{'
                else:
                    cur_str += '"'
            else:
                cur_str += l[i]
        
        if cur_str:
            if stack[index - 1] == '</' and stack[index] == '</':
                cur_str += INDENT * (open_tags - closed_tags - 1) + '},\n'
            elif stack[index] == '<' and stack[index + 1] == '<':
                cur_str += '\n'
            elif stack[index] == '</' and stack[index + 1] == '<':

                pass
                # cur_str += '"'
                # if stack[index] == '<':
                #     cur_str += ',\n'
                # else:
                #     cur_str += '\n'
        else:
            continue
        
        if l and l[0] != '<':
            json[-1] += cur_str + '"\n'
        else:
            json.append(cur_str)


    json.append('\n}')
    return json

