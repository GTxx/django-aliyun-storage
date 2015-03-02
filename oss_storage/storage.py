# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import mimetypes
from StringIO import StringIO

from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import File

from .oss.oss_api import OssAPI
from .utils import aliyun_setting


class AliyunOSSFile(File):

    def __init__(self, name, mode, storage):
        self.name = name
        self._storage = storage
        self._mode = mode
        self._file = None

    @property
    def file(self):
        if self._file:
            return self._file

        self._file = StringIO()
        if 'r' not in self._mode:
            raise IOError("mode {} is unable to read file".format(self._mode))
        bucket = self._storage.bucket
        res = self._storage.oss.get_object(bucket, self.name)
        if res not in (200,):
            raise IOError("read {} from {} fail: {}".format(self.name, bucket, res.read()))
        self._file.write(res.read())
        self._file.seek(0)
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @property
    def size(self):
        return self.file.len

    def read(self, *args, **kwargs):
        if 'r' not in self._mode:
            raise AttributeError("File was not opened in read mode.")
        return super(AliyunOSSFile, self).read(*args, **kwargs)

    def write(self, *args, **kwargs):
        raise NotImplementedError('file write is not supported yet')



class AliyunStorage(Storage):

    file_class = AliyunOSSFile
    access_id_name = 'ALIYUN_OSS_ACCESS_KEY_ID'
    access_key_name = 'ALIYUN_OSS_ACCESS_KEY_SECRETE'
    access_host_name = 'ALIYUN_OSS_ACCESS_HOST'
    bucket_name = 'ALIYUN_OSS_BUCKET_NAME'
    file_overwrite = aliyun_setting('ALIYUN_OSS_FILE_OVERWRITE', False)

    def __init__(self, bucket_name=None, access_id=None, access_key=None,
                 access_host=None):
        self.bucket_name = aliyun_setting(self.bucket_name, bucket_name)
        self.access_id = aliyun_setting(self.access_id_name, access_id)
        self.access_key = aliyun_setting(self.access_key_name, access_key)
        self.access_host = aliyun_setting(self.access_host_name, access_host)

        self.oss = OssAPI(self.access_host, self.access_id, self.access_key)
        self._bucket = None

    def _open(self, name, mode='rb'):
        cleaned_name = self._clean_name(name)
        f = self.file_class(cleaned_name, mode, self)
        return f

    def _save(self, name, content):
        cleaned_name = self._clean_name(name)
        # TODO: suport gzip
        # content = self._compress(content)

        # TODO: support chunk storage, used in large file
        if hasattr(content, 'chunk'):
            content_str = ''.join(chunk for chunk in content.chunks())
        else:
            content_str = content.read()
        content_type = mimetypes.guess_type(cleaned_name)[0] or "application/x-octet-stream"
        res = self.oss.put_object_from_string(self.bucket, cleaned_name, content_str, content_type)
        if res.status not in (200, 206):
            raise IOError('save in aliyun oss fail: {}'.format(res.read()))
        return cleaned_name

    def delete(self, name):
        response = self.oss.delete_object(self.bucket, name)
        if response.status != 204:
            raise IOError('delete {} in {} fail: {}'.format(name, self.bucket, response.read()))

    def exists(self, name):
        response = self.oss.head_object(self.bucket, name)
        if response.status == 200:
            return True
        else:
            print("object {} not exist: {}".format(name, response.read()))
            return False

    def listdir(self, path):
        return super(AliyunStorage, self).listdir(path)

    def size(self, name):
        response = self.oss.head_object(self.bucket, name)
        if response.status == 200:
            return response.getheader('content-length')
        else:
            raise IOError('get delete {} size fail: {}'.format(name, response.read()))

    def url(self, name):
        # TODO: 目前默认使用private的bucket，需要支持其他acl类型的bucket
        return self.oss.sign_url('GET', self.bucket, name, timeout=3600)

    @property
    def bucket(self):
        """
        Get the current bucket. If there is no current bucket object
        create it.
        """
        if self._bucket:
            return self._bucket
        res = self.oss.get_bucket(self.bucket_name)
        if res.status == 200:
            self._bucket = self.bucket_name
            return self._bucket
        res = self.oss.create_bucket(self.bucket_name)
        if res.status == 200:
            self._bucket = self.bucket_name
            return self._bucket
        else:
            raise ImproperlyConfigured('Create bucket fail, {}'.format(
                res.read()))

    def _clean_name(self, name):
        """
        Cleans the name so that Windows style paths work
        """
        # Useful for windows' paths
        return os.path.normpath(name).replace('\\', '/')

    def get_available_name(self, name):
        if self.file_overwrite:
            name = self._clean_name(name)
            return name
        return super(AliyunStorage, self).get_available_name(name)

    def modified_time(self, name):
        response = self.oss.head_object(self.bucket, name)
        if response.status == 200:
            return response.getheader('last-modified')
        else:
            raise IOError('get delete {} size fail: {}'.format(name, response.read()))
