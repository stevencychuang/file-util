import unittest
from fileutil import shutil, cp2dst, get_real_path, replace_dir_parts, Path, FileParser


class TestFunc(unittest.TestCase):

    def test_get_real_path(self):
        print(get_real_path("./"))

    def test_cp2dst(self):
        cp2dst(r"tmp\path\to\test3.py", "./temp2")

    def test_replace_dir_parts(self):
        dst = replace_dir_parts("C:\\system\\app", {0: "D:\\", 1: "workspace", 3: "fork"})
        print(dst)
        Path(dst)


class TestFileList(unittest.TestCase):

    def setUp(self):
        self.fileutil = FileParser("./tmp", "*.py")

    def test_init(self):
        print(self.fileutil._path)

    def test_get_dict(self):
        # test case: search for the files with "*.py"
        print(self.fileutil.get_dict())
        # test case: search for the folders with "path*""
        fileutil = FileParser("./tmp", "path*")
        print(fileutil.get_dict())

    def test_replace_dst(self):
        fileutil = FileParser("./tmp", "*.txt")
        fileutil.det_dst("./temp2")
        fileutil.replace_dst({"dir": "folder", "txt": "py"})
        print(fileutil.dict_dst)

    def test_cp2dst(self):
        # test case: without neither the input argument `root_dst`` nor calling det_dst first
        with self.assertRaises(Exception) as context:
            self.fileutil.cp2dst()
        print(context)

        # test case: with wrong type of the input argument `root_dst`
        with self.assertRaises(TypeError) as context:
            self.fileutil.cp2dst(1)
        print(context)

        # test case: samply using cp2dst() with the input argument `root_dst`
        print(self.fileutil.cp2dst("./temp2"))
        shutil.rmtree("./temp2")

        # test case: using cp2dst() after processing for destination
        fileutil = FileParser("./tmp", "*.py")
        fileutil.det_dst("./temp2")
        fileutil.replace_dst({"directory": "directory1", ".py": ".txt"})
        print(fileutil.cp2dst())
        shutil.rmtree("./temp2")
