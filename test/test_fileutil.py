import unittest
import shutil
from fileutil import cp2dst, get_real_path, replace_dir_parts, Path, FileParser


class TestFunc(unittest.TestCase):

    def test_get_real_path(self):
        print(get_real_path("./"))

    def test_cp2dst(self):
        cp2dst(r"test/tmp/path/to/test3.py", "test/temp2/test3.py")
        shutil.rmtree("test/temp2")

    def test_replace_dir_parts(self):
        dst = replace_dir_parts("C:\\system\\app", {0: "D:\\", 1: "workspace", 3: "fork"})
        print(dst)
        Path(dst)


class TestFileList(unittest.TestCase):

    def setUp(self):
        self.fileutil = FileParser("test/tmp", "*.py")

    def test_init(self):
        print(self.fileutil._path)

    def test_get_dict(self):
        # test case: search for the files with "*.py"
        print(self.fileutil.get_dict())
        # test case: search for the folders with "path*""
        fileutil = FileParser("test/tmp", "path*")
        print(fileutil.get_dict())

    def test_replace_dst(self):
        fileutil = FileParser("test/tmp", "*.txt")
        fileutil.det_dst("test/temp2")
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
        print(self.fileutil.cp2dst("test/temp2"))
        shutil.rmtree("test/temp2")

        # test case: using cp2dst() after processing for destination
        fileutil = FileParser("test/tmp", "*.py")
        fileutil.det_dst("test/temp2")
        fileutil.replace_dst({"directory": "directory1", ".py": ".txt"})
        print(fileutil.cp2dst())
        shutil.rmtree("test/temp2")

    def test_clone(self):
        parser1 = self.fileutil.clone()
        print(parser1._dict)
        print(parser1.dict_dst)

        self.fileutil.get_dict()
        parser2 = self.fileutil.clone()
        print(parser2._dict)
        print(parser2.dict_dst)

        self.fileutil.det_dst("test/temp2")
        parser3 = self.fileutil.clone()
        print(parser3._dict)
        print(parser3.dict_dst)
