from pathlib import Path
import shutil


def get_real_path(str_path: str):
    return str(Path(str_path).resolve())


class FileParser:

    def __init__(self, root, keyword):
        self.root = root
        self.keyword = keyword
        self._dict = None
        self._path = Path(root)

    def get_dict(self):
        if self._dict is None:
            self._dict = {}
            for path in self._path.rglob(self.keyword):
                self._dict[path] = path.name
                print(path.anchor)
        return self._dict

    def cp2dst(self, root_dst):
        for src in self.get_dict().keys():
            print(type(src))
            dst = str(src).replace(self.root, root_dst)
            print(dst)
            shutil.copy2(src, dst)
