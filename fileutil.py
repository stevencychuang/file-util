from pathlib import Path
import shutil
import os


def get_real_path(str_path: str):
    return str(Path(str_path).resolve())


def cp2dst(src, dst):
    """!
    Extension of shutil.copy that directory of destination will be created if it not exists.
    """
    dir_dst = os.path.dirname(dst)
    if not os.path.isdir(dir_dst):
        Path(dir_dst).mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)
    return dst


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
            dst = str(src).replace(self.root, root_dst)
            cp2dst(src, dst)
