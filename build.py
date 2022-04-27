"""
build.py

A simple script to build the project into a .zip file
"""

import os
import zipfile

exclude = [
    '__pycache__',
]


def path_full_split(path: str) -> list[str]:
    head, tail = os.path.split(path)
    if head == '':
        return [tail]
    return path_full_split(head) + [tail]


def walk_subdir(d: str) -> list[str]:
    results = []
    for dir_path, dirs, files in os.walk(d):
        for e in exclude:
            while e in dirs:
                dirs.remove(e)
        for f in files:
            path = os.path.join(dir_path, f)
            results.append(path)
    return results


def main():
    files = walk_subdir('src')

    z = zipfile.ZipFile('build.zip', 'w')
    for i, f in enumerate(files):
        print(f'{i/len(files):.0%}\r', end='')
        # Rename paths
        s = path_full_split(f)[1:]
        f_new = os.path.join('UniversalController', *s)
        z.write(f, f_new)
    z.close()
    print('Done!' + ' ' * 10)


if __name__ == "__main__":
    main()
