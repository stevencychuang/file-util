import unittest
from fileutil import FileParser


class TestFileList(unittest.TestCase):

    def setUp(self):
        self.fileutil = FileParser("D:\\workspaces\\file-util\\tmp", "*.py")

    def test_init(self):
        print(self.fileutil._path)

    def test_get_dict(self):
        print(self.fileutil.get_dict())

    def test_cp2dst(self):
        self.fileutil.cp2dst("temp2")
