import unittest
from fileutil import cp2dst, get_real_path, replace_dir_parts, Path, FileParser


class TestFunc(unittest.TestCase):

    def test_get_real_path(self):
        print(get_real_path("./"))

    def test_cp2dst(self):
        cp2dst(r"tmp\path\to\test2.py", "./temp2")
        
    def test_replace_dir_parts(self):
        dst = replace_dir_parts("C:\\system\\app", {0: "D:\\", 1: "workspace", 3: "fork"})
        print(dst)
        Path(dst)


class TestFileList(unittest.TestCase):

    def setUp(self):
        self.fileutil = FileParser(r".\tmp", "*.py")

    def test_init(self):
        print(self.fileutil._path)

    def test_get_dict(self):
        print(self.fileutil.get_dict())

    def test_cp2dst(self):
        self.fileutil.cp2dst("./temp2")
        
    def test_cp2dstex(self):
        depth_cwd = len(Path("./").absolute().parts)
        print(self.fileutil.cp2dstex("./temp2/temp1/temp3",
                                     up=1,
                                     depth_swap_dir_names=(depth_cwd + 0, depth_cwd + 1)))
