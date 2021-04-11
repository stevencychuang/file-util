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
    return str(dst)


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
                self._dict[get_real_path(str(path))] = path.name
        return self._dict

    def get_list(self):
        return list(self.get_dict().keys())

    def get_list_dir(self, up=0):
        return list(map(lambda p: Path(p).parents[up], self.get_list()))

    def cp2dst(self, root_dst):
        list_dst = []
        for src in self.get_dict().keys():
            dst = str(src).replace(self.root, root_dst)
            list_dst.append(cp2dst(src, dst))
        return list_dst

    def cp2updst(self, root_dst, up=0):
        list_dst = []
        for src, name in self.get_dict().items():
            dst = str(src).replace(self.root, root_dst)
            dir_dst = Path(dst).parents[up]
            list_dst.append(cp2dst(src, dir_dst / name))
        return list_dst
