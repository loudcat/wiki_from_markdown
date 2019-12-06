import os
import re
import time
from pathlib import Path


def branch(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        data = func(*args, **kwargs)
        end = time.time()
        work_time = end - start
        return {'data': data, 'time': work_time}

    return wrapper


def get_tree(_dir, level=0):
    node = []
    for item in Path(_dir).iterdir():
        if item.is_file():
            node.append({'name': item.name, 'type': 'file', 'link': '/' + item.as_posix()})
            print(f'{"-" * level}{item.name}')
        else:
            print(f'{"-" * level}d\'{item.name}')
            node.append(
                {'name': item.name, 'type': 'dir', 'parent': get_tree(item, level=level + 1)})
    return node


@branch
def search_in_files(_dir, word):
    reg_exp = re.compile(r'({})'.format(word), flags=re.IGNORECASE)
    res = []
    for file in Path(_dir).rglob('*.*'):
        # if r.search(file.name):
        #     res.append({'file': r.sub(r'<b>\1</b>',file.name), 'lines': []})

        if os.stat(str(file)).st_size > 0:
            with open(str(file)) as open_file:  # , mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
                for line in open_file.readlines():
                    if reg_exp.search(line):
                        try:
                            fa = next(item for item in res if reg_exp.sub(r'<b>\1</b>', str(file)) == item['file'])
                            fa['lines'].append(reg_exp.sub(r'<b>\1</b>', line))
                        except StopIteration:
                            res.append(
                                {'file': reg_exp.sub(r'<b>\1</b>', str(file)),
                                 'href': '/' + str(file),
                                 'lines': [reg_exp.sub(r'<b>\1</b>', line)]}
                            )
    return res

# if __name__ == '__main__':
#     # node = get_tree('example_dir')
#     # print(node)
#     r = search_in_files('example_dir', 'test')
#     print(r)
