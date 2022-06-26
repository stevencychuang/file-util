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


def replace_dir_parts(src: str, dst_parts: dict):
    """
    To replace the parts of the source path with specific depths.
    For example, if you want to replace "C:\\system\\app\\origin" with "D:\\workspace\\app\\fork".
    The usage will be replace_dir_parts("C:\\system\\app", {0: "D:\\", 1: "workspace", 3: "fork"}).

    Args:
        src (str): the source path
        dst_parts (dict): the expected parts to replace the source path

    Returns:
        str: the target path
    """
    dst = [dst_parts[i] if i in dst_parts.keys() else part
           for i, part in enumerate(Path(src).parts)]
    return str(dst)


class FileParser:

    def __init__(self, root, keyword: str, how="default"):
        """The object to manage files' structure with defining the root folder and keyword.
        The keyword could be for the names of files or folders

        Args:
            root (_type_): the root directory to be parsed recursively
            keyword (str): the keyword for searching recursively
            how (str): the method to search keyword. "default": use pathlib rglob, "regrex": use re search(TO-DO)
        """
        self.root = root
        self.keyword = keyword
        self._path = Path(root)
        self._dict: dict = None
        self.dict_dst: dict = None

    def get_dict(self):
        """To get the dictionary of the parsed structure as {path1: name1, path2: name2, ...}
        Returns:
            _type_: the dictionary of the parsed structure
        """
        if self._dict is None:
            self._dict = {}
            for path in self._path.rglob(self.keyword):
                str_path = get_real_path(str(path))
                self._dict[str_path] = path.name
        return self._dict

    def get_dict_inv(self):
        """To get the inverse dictionary of the parsed structure as {name1: path1, name2: path2, ...}

        Returns:
            _type_: the inverse dictionary of the parsed structure
        """
        _dict = self.get_dict()
        return dict(zip(_dict.values(), _dict.keys()))

    def get_list(self):
        """To get the list of the parsed structure as [path1, path2, ...]

        Returns:
            _type_: _description_
        """
        return list(self.get_dict().keys())

    def get_list_dir(self, up=0):
        """To get the list of the parsed structure which are directories.
        User can define the up levels.
        For example, [/dir1/dir2/dir3, /dir1/dir2] will be [/dir1/dir2, /dir1] with up=1.

        Args:
            up (int, optional): the elevated levels. Defaults to 0.

        Returns:
            _type_: _description_
        """

        return list(map(lambda p: Path(p).parents[up], self.get_list()))

    def det_dst(self, root_dst: str):
        """The function to determine the destination which the structure will be copyied to.

        Args:
            root_dst (str): the root directory of the destination
        """
        root_dst_str = str(Path(root_dst))
        self.dict_dst = {}
        for src in self.get_dict().keys():
            dst = str(src).replace(str(self._path), root_dst_str)
            self.dict_dst[src] = dst

    def replace_dst(self, replace: dict):
        """The function to replace some keywords in the path with specific name.
        For example, if the destination path is "/dir1/dir2/test.txt".
        It will be "/folder1/folder2/test.py" with replace = {"dir": "folder", "txt": "py"}

        Args:
            replace (dict): the keywords to be replace with specific names
        """
        for src in self.dict_dst.keys():
            path_dst = str(Path(self.dict_dst[src]))
            if isinstance(replace, dict):
                for k, v in replace.items():
                    path_dst = path_dst.replace(k, v)
            self.dict_dst[src] = path_dst

    def swap_dir_names(self, depth_swap_dir: tuple):
        """
        The function to swap the directory names.
        For example, "C:\\system\\app\\origin\\file1" will be "C:\\origin\\app\\system\\file1" if depth_swap_dir_names=(1, 3).

        Args:
            depth_swap_dir (tuple): the tuple of diretories depth to swap.
        """
        for src in self.dict_dst.keys():
            dst = Path(self.dict_dst[src])
            dir_dst = dst.parents[0]
            temp_swap = list(dir_dst.parts)
            temp_swap[depth_swap_dir[0]], temp_swap[depth_swap_dir[1]] = temp_swap[depth_swap_dir[1]], temp_swap[depth_swap_dir[0]]
            dir_dst = Path(*temp_swap)
            self.dict_dst[src] = dir_dst

    def cp2dst(self, root_dst: str = None) -> list:
        """
        The function to copy the files from source structure to destination structure.

        Args:
            root_dst (str, optional): the destination root. Defaults to None.

        Returns:
            list: the list of the path for destination results after copying
        """
        # The input type and self.dict_dst status checking
        if isinstance(root_dst, str):
            self.det_dst(root_dst)
        elif root_dst is None and isinstance(self.dict_dst, dict):
            pass
        elif root_dst is None and self.dict_dst is None:
            raise Exception("Please define root_dst or call det_dst(root_dst) first")
        else:
            raise TypeError("The type of the input argument `root_dst` is not correct")

        # The process of copying from source to destination
        list_dst = []
        for src in self.dict_dst.keys():
            list_dst.append(cp2dst(src, self.dict_dst[src]))
        return list_dst

    def clone(self) -> "FileParser":
        """Get the clone of FileParser()

        Returns:
            FileParser: the cloned one
        """
        parser = FileParser(self.root, self.keyword)
        if isinstance(self._dict, dict):
            parser._dict = self._dict
        if isinstance(self.dict_dst, dict):
            parser.dict_dst = self.dict_dst
        return parser
