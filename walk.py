""" functions for work with directory """
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
    """ Return tree of directory for sidebar menu """
    node = list()
    for item in Path(_dir).iterdir():
        if item.is_file():
            node.append({'name': item.name, 'type': 'file', 'link': '/' + item.as_posix()})
            #print(f'{"-" * level}{item.name}')
        else:
            #print(f'{"-" * level}d\'{item.name}')
            node.append(
                {'name': item.name, 'type': 'dir', 'parent': get_tree(item, level=level + 1)})
    return node


@branch
def search_in_files(_dir, word):
    """ Search """
    reg_exp = re.compile(r'({})'.format(word), flags=re.IGNORECASE)
    response = []
    for file in Path(_dir).rglob('*.md'):
        if file.stat().st_size > 0:
            with file.open() as open_file:
                for line in open_file.readlines():
                    if reg_exp.search(line):
                        try:
                            fa = next(item for item in response if reg_exp.sub(r'<b>\1</b>', str(file)) == item['file'])
                            fa['lines'].append(reg_exp.sub(r'<b>\1</b>', line))
                        except StopIteration:
                            response.append(
                                {
                                    'file': reg_exp.sub(r'<b>\1</b>', str(file)),
                                    'href': '/' + str(file),
                                    'lines': [reg_exp.sub(r'<b>\1</b>', line)]
                                }
                            )
    return response
