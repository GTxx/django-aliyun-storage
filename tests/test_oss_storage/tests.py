from django.test import TestCase
from oss_storage.storage import AliyunStorage
import tempfile
import os


def get_filename(f):
    return os.path.basename(f.name)


class OSSTestCase(TestCase):

    def test_init(self):
        obj = AliyunStorage()
        self.assertEqual(type(obj), AliyunStorage)

    def test_save(self):
        obj = AliyunStorage()
        with tempfile.NamedTemporaryFile() as f:
            fname = get_filename(f)
            res = obj._save(fname, f)
            self.assertEqual(res, fname)

    def test_exist(self):
        obj = AliyunStorage()
        with tempfile.NamedTemporaryFile() as f:
            fname = get_filename(f)
            res = obj._save(fname, f)
            print(obj.exists(fname))
            self.assertEqual(obj.exists(fname), True)

    def test_delete(self):
        obj = AliyunStorage()
        with tempfile.NamedTemporaryFile() as f:
            fname = get_filename(f)
            res = obj._save(fname, f)
            self.assertEqual(obj.delete(fname), None)
