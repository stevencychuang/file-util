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

    def __init__(self, root, keyword: str, how: str):
        """_summary_

        Args:
            root (_type_): the root directory to recursive
            keyword (str): the keyword to recursive search
            how (str): the method to search keyword. "default": use pathlib rglob, "regrex": use re search
        """
        self.root = root
        self.keyword = keyword
        self._dict: dict = None
        self.dict_dst: dict = None
        self._path = Path(root)

    def get_dict(self):
        if self._dict is None:
            self._dict = {}
            for path in self._path.rglob(self.keyword):
                str_path = get_real_path(str(path))
                self._dict[str_path] = path.name
        return self._dict

    def get_dict_inv(self):
        _dict = self.get_dict()
        return dict(zip(_dict.values(), _dict.keys()))

    def get_list(self):
        return list(self.get_dict().keys())

    def get_list_dir(self, up=0):
        return list(map(lambda p: Path(p).parents[up], self.get_list()))

    def det_dst(self, root_dst):
        root_dst_str = str(Path(root_dst))
        for src in self.get_dict().keys():
            dst = str(src).replace(str(self._path), root_dst_str)
            self.dict_dst[src] = dst

    def replace_dst(self, replace: dict):
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

    def cp2dst(self):
        list_dst = []
        for src in self.dict_dst.keys():
            list_dst.append(cp2dst(src, self.dict_dst[src]))
        return list_dst
