import unittest
from fileutil import cp2dst, get_real_path, FileParser


class TestFunc(unittest.TestCase):

    def test_get_real_path(self):
        print(get_real_path("./"))

    def test_cp2dst(self):
        cp2dst(r"tmp\path\to\test2.py", "./temp2")


class TestFileList(unittest.TestCase):

    def setUp(self):
        self.fileutil = FileParser(r"D:\workspaces\file-util\tmp", "*.py")

    def test_init(self):
        print(self.fileutil._path)

    def test_get_dict(self):
        print(self.fileutil.get_dict())

    def test_cp2dst(self):
        self.fileutil.cp2dst("./temp2")
