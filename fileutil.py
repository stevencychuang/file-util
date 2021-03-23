from pathlib import Path

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
        return self._dict
