from pathlib import  Path
import mmap
import os
import re


def branch(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        data = func(*args, **kwargs)
        end = time.time()
        t = end - start
        return {'data': data, 'time': t}
    return wrapper


def get_tree(_dir, level=0):
    node = []
    for item in Path(_dir).iterdir():
        if item.is_file():
            node.append({'name': item.name, 'type': 'file', 'link': '/' + item.as_posix()})
            print(f'{"-"*level}{item.name}')
        else:
            print(f'{"-"*level}d\'{item.name}')
            node.append({'name': item.name, 'type': 'dir', 'parent': get_tree(item, level=level+1)})
    return node

@branch
def search_in_files(_dir, word):
    r = re.compile(r'({})'.format(word), flags=re.IGNORECASE)
    res = []
    for file in Path(_dir).rglob('*.*'):
        # if r.search(file.name):
        #     res.append({'file': r.sub(r'<b>\1</b>',file.name), 'lines': []})

        if os.stat(str(file)).st_size > 0:
            with open(str(file)) as f: #, mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as s:
                for line in f.readlines():
                    if r.search(line):
                        try:

                            fa = next(item for item in res if r.sub(r'<b>\1</b>', str(file)) == item['file'])
                            fa['lines'].append(r.sub(r'<b>\1</b>', line))
                        except StopIteration:
                            res.append({'file': r.sub(r'<b>\1</b>', str(file)), 'href': '/' + str(file), 'lines': [r.sub(r'<b>\1</b>', line)]})
    return res

if __name__ == '__main__':
    # node = get_tree('wiki')
    # print(node)
    r = search_in_files('wiki', 'test')
    print(r)