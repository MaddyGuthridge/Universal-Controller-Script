
import os
import zipfile

top_include = [
    'common',
    'controlsurfaces',
    'devices',
    'fl_typing',
    'plugs',
    'resources',
    'config.py',
    'device_eventforward.py',
    'device_universal.py',
    'LICENSE',
]

exclude = [
    '__pycache__',
]


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
    files: list[str] = []
    for d in os.listdir('.'):
        if d in top_include:
            os.
            files += walk_subdir(os.path.join('.', d))

    for f in os.scandir()

    z = zipfile.ZipFile('build.zip', 'w')
    for f in files:
        z.write(f)
    z.close()


if __name__ == "__main__":
    main()
